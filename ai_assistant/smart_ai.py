import requests
import os
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_groq_client():
    return Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You are CampSpark AI — advanced College ERP assistant.

CORE BEHAVIOR:

1️⃣ You answer ALL academic, programming, and general knowledge questions.

2️⃣ If user asks coding question:
- Provide full working code
- Explain line by line
- If debugging → explain error + fix
- Use clean formatting

3️⃣ If user asks Computer Science theory:
- Give structured explanation
- Use headings
- Use examples

4️⃣ If user asks about CampSpark:
- Answer using ERP context (attendance, fees, marks, events, complaints, etc.)
- Never invent fake data.

5️⃣ Language Rule:
Reply in the same language used by the user.

6️⃣ Style:
- Clear
- Structured
- Bullet points when needed
- Professional but student-friendly

7️⃣ Formatting Rule:
- Use proper headings (use plain text headings without excessive #)
- Use bullet points using - or •
- Avoid too many markdown symbols like ### or **
- Write clean formatted response suitable for web chat

You are intelligent, helpful, and technical.
"""


def local_ai_fallback(text):
    t = text.lower()

    if "attendance" in t:
        return "You can check attendance from your dashboard."
    if "fee" in t:
        return "Please check the fee section for pending amount."
    if "exam" in t:
        return "Focus on revision and previous questions."
    if "hello" in t or "hi" in t:
        return "Hello 🙂 How can I help you?"
    if "event" in t:
        return "Check events section for latest updates."

    return "Tell me more. I'm here to help."


def smart_ai_response(message, role="student", history=None):

    if not message.strip():
        return "Please type something."

    # =============================
    # 🔥 PRIORITIZE CODING QUESTIONS
    # =============================
    lower_msg = message.lower()

    if any(word in lower_msg for word in
           ["code", "python", "java", "c++", "debug", "error", "html", "css", "javascript"]):

        message = (
            "User is asking a programming question. "
            "Provide full working code, debugging steps, and explanation.\n\n"
            + message
        )

    # =============================
    # 🔍 Detect "Only Code" Request
    # =============================
    lower_msg = message.lower()

    only_code_request = any(
        phrase in lower_msg for phrase in [
            "only code",
            "code only",
            "give only",
            "no explanation",
            "just code"
        ]
    )

    if only_code_request:
        message = message + "\n\nIMPORTANT: Return ONLY the code. Do NOT add explanation. Do NOT add extra text."

    # =============================
    # BUILD MESSAGE MEMORY
    # =============================
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    if history:
        for h in history[-6:]:
            messages.append({
                "role": h.get("role", "user"),
                "content": h.get("content", "")
            })

    messages.append({
        "role": "user",
        "content": message
    })

    # =============================
    # GROQ PAYLOAD
    # =============================
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "temperature": 0.6
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=15
        )

        data = r.json()

        if "choices" in data:
            return data["choices"][0]["message"]["content"]

    except Exception:
        pass

    return local_ai_fallback(message)