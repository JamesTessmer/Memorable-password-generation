from flask import Flask, render_template, request, session
from dotenv import load_dotenv
import random
import os

app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv("FLASK_APP_KEY") #you'll need to make a .env file with this variable
all_questions = [
    {"label": "What is your name?", "name": "name"},
    {"label": "What is your favorite color?", "name": "color"},
    {"label": "What is your favorite food?", "name": "food"},
    {"label": "What is your hobby?", "name": "hobby"},
    {"label": "Where are you from?", "name": "location"},
]
    
    #randomly select x questions to show. We can probably prompt the user for
    # a number of words they want to have in the passphrase and select that many questions
def generate_questions():
    return random.sample(all_questions, 3)

@app.route("/", methods=["GET", "POST"])
def index():
    if "questions" not in session:
        session["questions"] = generate_questions()

    questions = session["questions"]

    if request.method == "POST":

        # If Reset button was pressed we show new questions
        if request.form.get("action") == "reset":
            session["questions"] = generate_questions()
            return render_template("index.html",
                                   questions=session["questions"],
                                   answers=None)

        # If Submit button was pressed we process answers in the text boxes
        if request.form.get("action") == "submit":
            answers = {q["name"]: request.form.get(q["name"]) for q in questions}
            return render_template("index.html",
                                   questions=questions,
                                   answers=answers)

    return render_template("index.html",
                           questions=questions,
                           answers=None)

if __name__ == "__main__":
    app.run(debug=True)