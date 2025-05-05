import csv
from flask import Blueprint, render_template, request, redirect, url_for
from app.analysis import analyze_question_answer  # Ensure correct import

main_bp = Blueprint("main", __name__)

def load_questions():
    try:
        with open("app/data/questions.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            print("CSV Headers:", reader.fieldnames)  # Debugging headers
            
            questions_list = []
            for row in reader:
                print("Raw Row Data:", row)  # Debugging output
                
                # Ensure the correct columns exist
                if {"question", "key_phrases", "feedback", "correct_answer"}.issubset(row):
                    questions_list.append({
                        "question": row["question"].strip(),
                        "key_phrases": [phrase.strip().lower() for phrase in row["key_phrases"].split(";")],
                        "feedback": row["feedback"].strip(),
                        "correct_answer": row["correct_answer"].strip()  # Load correct answer
                    })
                else:
                    print(f"Skipping invalid row: {row}")

            if not questions_list:
                print("Warning: No valid questions found in CSV.")
            return questions_list
    except FileNotFoundError:
        print("Error: questions.csv not found!")
        return []

# Load questions globally
questions = load_questions()
current_index = 0  # Track current question index

@main_bp.route("/")
def home():
    """
    Renders the home page with the first question.
    """
    global current_index
    if not questions:
        return "No questions found! Please upload a valid questions.csv file."
    
    return render_template("index.html", question=questions[current_index], feedback=None, show_next=False)

@main_bp.route("/analyze", methods=["POST"])
def analyze():
    """
    Analyzes the user's answer and provides feedback.
    """
    global current_index
    if not questions:
        return redirect(url_for("main.home"))

    question = request.form.get("question")
    answer = request.form.get("answer")

    if not question or not answer:
        return redirect(url_for("main.home"))

    # Get analysis results
    analysis = analyze_question_answer(question, answer)

    feedback = analysis.get("feedback", "No feedback available")
    detailed_feedback = analysis.get("detailed_feedback", "")
    suggested_answer = analysis.get("suggested_answer", "")  # Fix: Use suggested_answer instead of correct_answer

    print("DEBUG: Passing to template:", feedback, detailed_feedback, suggested_answer)  # Debugging

    return render_template(
        "index.html",
        question=questions[current_index],
        feedback=feedback,
        detailed_feedback=detailed_feedback,
        suggested_answer=suggested_answer,  # Ensure it's passed correctly
        show_next=True
    )



@main_bp.route("/next", methods=["POST"])
def next_question():
    """
    Moves to the next question in the list.
    """
    global current_index
    if not questions:
        return redirect(url_for("main.home"))

    current_index = (current_index + 1) % len(questions)
    return redirect(url_for("main.home"))
