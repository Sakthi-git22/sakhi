import csv
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import os

nltk_data_path = os.path.expanduser('~/nltk_data')
if not os.path.exists(nltk_data_path):
    nltk.download('vader_lexicon')

# Ensure NLTK dependencies are downloaded
nltk.download("vader_lexicon")

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# Load questions and key phrases from CSV
def load_questions_feedback():
    questions = []
    try:
        with open("app/data/questions.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            required_headers = {"question", "key_phrases", "feedback", "correct_answer"}
            if not reader.fieldnames or not required_headers.issubset(set(reader.fieldnames)):
                print("Error: CSV is missing required headers!")
                return []

            for row in reader:
                question = row.get("question", "").strip()
                key_phrases = row.get("key_phrases", "").strip()
                feedback = row.get("feedback", "").strip()
                correct_answer = row.get("correct_answer", "").strip()  # Ensure correct answer is loaded

                key_phrases_list = [phrase.strip().lower() for phrase in key_phrases.split(";") if phrase.strip()]

                if question and key_phrases_list:
                    questions.append({
                        "question": question,
                        "key_phrases": key_phrases_list,
                        "feedback": feedback,
                        "correct_answer": correct_answer  # Store correct answer
                    })

    except FileNotFoundError:
        print("Error: questions.csv file not found!")
    except Exception as e:
        print(f"Error loading CSV: {e}")

    return questions


def analyze_question_answer(question, answer):
    questions_list = load_questions_feedback()

    if not questions_list:
        return {
            "feedback": "No questions found. Please upload a valid questions.csv file.",
            "detailed_feedback": "",
            "suggested_answer": ""
        }

    for q in questions_list:
        if q["question"] == question:
            key_phrases = q["key_phrases"]
            feedback = q["feedback"]
            correct_answer = q["correct_answer"]  # Extract correct answer

            correct = any(phrase in answer.lower() for phrase in key_phrases)

            if correct:
                return {
                    "feedback": "Correct answer!",
                    "detailed_feedback": feedback,
                    "suggested_answer": ""
                }
            else:
                return {
                    "feedback": "Incorrect answer.",
                    "detailed_feedback": f"Hint: {feedback}",
                    "suggested_answer": f"The correct answer is: {correct_answer}"  # Return correct answer
                }

    return {
        "feedback": "Question not found.",
        "detailed_feedback": "",
        "suggested_answer": ""
    }