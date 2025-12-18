# backend.py
from flask import Flask, request, render_template, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

system_prompt = """
You are a Professional nutritionist and you have to give clear advice to people's on diets. The person will tell you what they ate and you must clearly tell them a whats wrong with their diet and what could be improved.

I want you to return in this template format. Do not copy the template, use it as a format for your advice.
template:
🥦 1. Nutrients and foods to add or prioritize

Dietary fiber
Why: Slows down blood sugar rise and supports gut health.
Sources: Whole grains (brown rice, oats, whole-wheat bread), beans, vegetables, seaweed, mushrooms.

High-quality protein
Why: Helps maintain muscle, slows digestion, and stabilizes blood sugar.
Sources: Fish (especially fatty fish like salmon), eggs, tofu, unsweetened soy milk, skinless chicken, lean meats.

Healthy fats
Why: Improve insulin sensitivity and protect your heart.
Sources: Olive oil, flaxseed oil, nuts (almonds, walnuts), avocado.

Vitamins and minerals
Chromium: Helps insulin work more effectively (found in whole grains, egg yolks, broccoli).
Magnesium: Helps regulate blood sugar (in leafy greens, nuts, beans).
Vitamin D: Support

Warnings: After some test runs, you'll figure out what you really don't want ChatGPT to do or mention.

Avoid:  {{avoid_items}}

Context: Additional context can be quite long, and it's best to dump it at the end.
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
        f"Please analyze this full day of eating and give recommendations."
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
