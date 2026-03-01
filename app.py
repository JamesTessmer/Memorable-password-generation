from flask import Flask, render_template, request, session
from dotenv import load_dotenv
import json
import random
import os
#
# To do, on startup show a 'form' that prompts the user for the number of questions, and level of complexity they want in the password
# Add a button that lets users go back to that form
#
app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv("FLASK_APP_KEY") #you'll need to make a .env file with this variable

#read in questions
questions = []
with open("questions.json", "r") as f:
    data = json.load(f)
    questions = list(data.values())

join_chars = ['-','_','+','&','$','#','@','!','%','^','*','=']

    
#randomly select x questions to show based on user input
def generate_questions(num_questions: int):
    return random.sample(questions, num_questions)

#generate a password based on user answers to questions, with complexity adding varying characters
def generate_password(answers: dict, complexity: int):
    password = ""
    for val in answers.values():
        password = password + random.choice(join_chars) + val
    #replace white space characters since most websites, pages, etc. don't allow them
    password = password.replace(" ","")
    return password

@app.route("/", methods=["GET", "POST"])
def index():
    if "num_questions" not in session:
        session["num_questions"] = 3
    if "complexity" not in session:
        session["complexity"] = 1
    if "questions" not in session:
        session["questions"] = generate_questions(3)

    questions = session["questions"]

    if request.method == "POST":

        #update complexity and number of questions
        if request.form.get("action") == "update_settings":
            num_q = request.form.get("num_questions")
            complexity = request.form.get("complexity")
            #see if the values entered were integers (They may not be on app start up)
            existing_num_q = session["num_questions"]
            try:
                session["num_questions"] = int(num_q) if num_q else 3
            except ValueError:
                session["num_questions"] = 3

            try:
                session["complexity"] = int(complexity) if complexity else 1
            except ValueError:
                session["complexity"] = 1

            # Regenerate question only if the number of questions field changed
            if session['num_questions'] != existing_num_q:
                print(type(num_q))
                print(type(existing_num_q))
                session["questions"] = generate_questions(session["num_questions"])
            return render_template("index.html",
                                   questions=session["questions"],
                                   num_questions=session["num_questions"],
                                   complexity=session["complexity"],
                                   password=None)


        # If Reset button was pressed we show new questions
        elif request.form.get("action") == "reset":
            session["questions"] = generate_questions(session["num_questions"])
            return render_template("index.html",
                                   questions=session["questions"],
                                   num_questions=session["num_questions"],
                                   complexity=session["complexity"],
                                   password=None)

        # If Submit button was pressed we process answers in the text boxes
        elif request.form.get("action") == "submit":
            answers = {q["id"]: request.form.get(q["id"]) for q in questions}
            password = generate_password(answers, session['complexity'])
            return render_template("index.html",
                                   questions=session["questions"],
                                   num_questions=session["num_questions"],
                                   complexity=session["complexity"],
                                   password=password)

    return render_template("index.html",
                           questions=questions,
                           answers=None)

if __name__ == "__main__":
    app.run(debug=True)