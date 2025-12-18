# backend.py
from flask import Flask, request, render_template, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# SIMPLIFIED SYSTEM PROMPT
system_prompt = """
You are a nutrition coach.

Your job:
- Give SIMPLE, CLEAR, and SHORT feedback.
- Write for someone with no nutrition background.
- Avoid scientific terms unless absolutely necessary.
- Keep total response under 150 words.

Use this format ONLY:

✅ What you did well
- 2–3 short bullet points

⚠️ What could be improved
- 2–3 short bullet points

🥗 Simple suggestions for tomorrow
- 2–3 very easy, realistic suggestions

Nutrients Gaining:
- List nutrients they gain

Nutrients Missing:
- List missing essential nutrients

Rules:
- Do NOT lecture
- Do NOT mention micronutrients by name
- Do NOT give medical advice
- Be supportive and practical
"""

chat_history = [{"role": "system", "content": system_prompt}]

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    info_prompt = request.form.get("info")
    breakfast_prompt = request.form.get("breakfast")
    lunch_prompt = request.form.get("lunch")
    dinner_prompt = request.form.get("dinner")
    snack_prompt = request.form.get("snacks")

    user_prompt = (
        f"User Info: {info_prompt}\n"
        f"Breakfast: {breakfast_prompt}\n"
        f"Lunch: {lunch_prompt}\n"
        f"Dinner: {dinner_prompt}\n"
        f"Snacks: {snack_prompt}\n"
        f"Give simple daily food feedback."
    )

    chat_history.append({"role": "user", "content": user_prompt})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=chat_history
    )

    assistant_response = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": assistant_response})

    return jsonify({"response": assistant_response})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
