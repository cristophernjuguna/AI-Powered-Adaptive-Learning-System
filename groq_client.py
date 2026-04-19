import httpx
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "meta-llama/llama-prompt-guard-2-86m")
GROQ_TIMEOUT_S = int(os.getenv("GROQ_TIMEOUT_S", 10))


async def call_groq(prompt: str) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful tutor."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 300,
    }

    async with httpx.AsyncClient(timeout=GROQ_TIMEOUT_S) as client:
        resp = await client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()

    return data["choices"][0]["message"]["content"]


def build_wrong_answer_prompt(topic: str, question: str, student_answer: str, correct_answer: str) -> str:
    return f"""
You are an empathetic tutor helping a student learn {topic}.

The question is:
"{question}"

The student chose:
"{student_answer}"

The correct answer is:
"{correct_answer}"

Please respond in this structure:
1. Explanation
2. Example
3. Follow-up question
4. Rubric

Keep it concise, helpful, and beginner-friendly.
"""


def build_correct_answer_prompt(topic: str, question: str, student_answer: str) -> str:
    return f"""
You are congratulating a student who just answered a {topic} question correctly.

The question was:
"{question}"

The student chose:
"{student_answer}"

Please respond in this structure:
1. Praise
2. Challenge question
3. Next-step tips

Keep it short, encouraging, and clear.
"""


def build_new_question_prompt(topic: str, difficulty: str = "easy", num_choices: int = 4) -> str:
    return f"""
Generate one quiz question for topic "{topic}" at difficulty "{difficulty}".

Return ONLY JSON in this exact format:
{{
  "question": "question text",
  "choices": ["A) ...", "B) ...", "C) ...", "D) ..."],
  "correct_index": 0,
  "explanation": "short explanation"
}}

Rules:
- Exactly {num_choices} choices.
- Keep it concise.
- No extra text outside JSON.
"""