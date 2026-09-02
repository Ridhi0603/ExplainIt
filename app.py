from google import genai
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()

api_key = os.getenv("gemini_api_key")

client = genai.Client(api_key=api_key)

MODEL = "gemini-3.6-flash"

def init_db():
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            concept TEXT,
            difficulty TEXT,
            explanation TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            history_id INTEGER,
            feedback TEXT
            )
    """)

    conn.commit()
    conn.close()

init_db()

def save_history(concept, difficulty, explanation):
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO history (concept, difficulty, explanation) VALUES (?, ?, ?)",
        (concept, difficulty, explanation)
    )

    conn.commit()

    history_id = cursor.lastrowid

    conn.close()

    return history_id

def get_history():
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, concept, difficulty, explanation FROM history ORDER BY id DESC")

    history = cursor.fetchall()

    conn.close()

    return history

def get_explanation(history_id):
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT explanation FROM history WHERE id = ?",
        (history_id,)
    )

    result = cursor.fetchone()

    conn.close()

    return result

def delete_history(history_id):
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM history WHERE id = ?",
        (history_id,)
    )

    conn.commit()
    conn.close()

def save_feedback(history_id, feedback):
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO feedback (history_id, feedback) VALUES (?, ?)",
        (history_id, feedback)
    )

    conn.commit()
    conn.close()

def handle_api_error(e):
    error_message = str(e)

    if "429" in error_message:
        return "ERROR_429"

    return "ERROR_GENERIC"

def create_exp(concept, difficulty):

    if not concept:
        return "Please enter a valid concept."

    if difficulty not in ["beginner", "student", "advanced"]:
        return "Please enter a valid difficulty level."

    prompt = f"""
    Explain {concept} at a {difficulty} level.

    Format your answer using exactly these five sections, in exactly this specific order:

    📘 Explanation:
    Give a clear explanation.

    🌍 Real-world analogy:
    Give one analogy.

    💻 Example:
    Give one example.

    ⚠️ Common mistakes:
    List common mistakes students make.

    📝 Practice questions:
    Give two-five practice questions.
    Do not provide the answers.
    Each question must be written on a single line.
    Do not use markdown code formatting.
    Do not add blank lines between questions.

    Do not change, remove, or rename the section headings under any circumstances.
    """

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        return response.text

    except Exception as e:
        return handle_api_error(e)

def check_answers(concept, questions, answers):

    prompt = f"""
    Check the student's answers for the concept: {concept}

    Questions:
    {questions}

    Student's answers:
    {answers}

    For each question:
    - Judge the student's answer based on whether it demonstrates the correct concept or understanding.
    - Do not require the student's wording to exactly match an expected answer.
    - Treat answers with different wording but the same correct meaning as correct.
    - Do not mark an answer wrong merely because it is shorter or phrased differently, as long as the core idea is correct.
    - Say whether the answer is correct or incorrect.
    - If incorrect, give the correct answer.
    - Give a brief explanation.

    At the end, give the student's score.
    """

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        return response.text

    except Exception as e:
        return handle_api_error(e)
    
def exp_diff(concept, difficulty, style):

    if difficulty not in ["beginner", "student", "advanced"]:
        return "Please enter a valid difficulty level."

    prompt = f"""
    Explain {concept} at a {difficulty} level.

    The student wants the explanation in this style: {style}

    Format your answer using exactly these five sections, in exactly this specific order:

    📘 Explanation:
    Explain the concept according to the requested style.

    🌍 Real-world analogy:
    Give one analogy.

    💻 Example:
    Give one example.

    ⚠️ Common mistakes:
    List common mistakes students make.

    📝 Practice questions:
    Give two practice questions.
    Do not provide the answers.
    Each question must be written on a single line.
    Do not use markdown code formatting.
    Do not add blank lines between questions.

    Do not change, remove, or rename the section headings under any circumstances.
    """
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        return response.text

    except Exception as e:
        return handle_api_error(e)