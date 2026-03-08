from flask import Flask, render_template, request, session
from dotenv import load_dotenv
import json
import random
import os
import math
import string

app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv("FLASK_APP_KEY")

#read in questions
questions = []
with open("questions.json", "r") as f:
    data = json.load(f)
    questions = list(data.values())

join_chars = ['-','_','+','&','$','#','@','!','%','^','*','=','?','>','<',',','.']
    
#randomly select x questions to show based on user input
def generate_questions(num_questions: int):
    return random.sample(questions, num_questions)

num_changes = {'a': '4', 'b': '8', 'e': '3', 'g': '6', 'i': '1', 'o': '0', 's': '5', 't': '7', 'z': '2'}
symbol_changes = {'a': '@', 'c': '(', 'h': '#', 's': '$', 't': '+'}

# Randomize the characters in the password with a given percentage (chance * 10)
def randomize_characters(password: str, chance: int):
    new = ""
    for character in password:
        if random.randrange(1, 11) <= chance and character.isalpha():
            # Change the character
            # Make lowercase for repeated pulls
            char = character.lower()
            if char in num_changes and char in symbol_changes:
                # Random chance between swapping case, making the letter a number, and making the letter a symbol
                rand = random.randrange(3)
                if rand == 0:
                    new = new + character.swapcase()
                elif rand == 1:
                    new = new + num_changes[char]
                else:
                    new = new + symbol_changes[char]
            elif char in num_changes:
                # Random chance between swapping case and making the letter a number
                if random.randrange(2) == 0:
                    new = new + character.swapcase()
                else:
                    new = new + num_changes[char]
            elif char in symbol_changes:
                # Random chance between swapping case and making the letter a symbol
                if random.randrange(2) == 0:
                    new = new + character.swapcase()
                else:
                    new = new + symbol_changes[char]
            else:
                # No special case, so change case of the letter
                new = new + character.swapcase()
        else:
            # Don't change the character (it's not a letter)
            new = new + character
    return new

#generate a password based on user answers to questions, with complexity adding varying characters
def generate_password(answers: dict, complexity: int):
    password = ""
    for val in answers.values():
        password = password + random.choice(join_chars) + randomize_characters(val, complexity)
    #replace white space characters since most websites, pages, etc. don't allow them
    password = password.replace(" ","")
    return password

#calculate and display entropy of the generated password
def calculate_entropy(password):
    if not password:
        return 0
    
    # Set pool of characters
    charset = 0
    if any(c in string.ascii_lowercase for c in password):
        charset += 26
    if any(c in string.ascii_uppercase for c in password):
        charset += 26
    if any(c in string.digits for c in password):
        charset += 10
    if any(c in string.punctuation for c in password):
        charset += 32 # Common punctuation/special chars
    
    # Base case for something funky happening
    if charset == 0:
        charset = 1
        
    # entropy = L * log2(R)
    length = len(password)
    entropy = length * math.log2(charset)
    
    #round the value for displaying
    return round(entropy, 2)
    

@app.route("/", methods=["GET", "POST"])
def index():
    if "num_questions" not in session:
        session["num_questions"] = 1
    if "complexity" not in session:
        session["complexity"] = 1
    if "questions" not in session:
        session["questions"] = generate_questions(1)

    questions = session["questions"]

    if request.method == "POST":

        #update complexity and number of questions
        if request.form.get("action") == "update_settings":
            num_q = request.form.get("num_questions")
            complexity = request.form.get("complexity")
            #see if the values entered were integers (They may not be on app start up)
            existing_num_q = session["num_questions"]
            try:
                session["num_questions"] = int(num_q) if num_q else 1
            except ValueError:
                session["num_questions"] = 1

            try:
                session["complexity"] = int(complexity) if complexity else 1
            except ValueError:
                session["complexity"] = 1

            # Regenerate question only if the number of questions field changed
            if session['num_questions'] != existing_num_q:
                session["questions"] = generate_questions(session["num_questions"])
            return render_template("index.html",
                                   questions=session["questions"],
                                   num_questions=session["num_questions"],
                                   complexity=session["complexity"],
                                   password=None,
                                   entropy=None)

        # If Reset button was pressed then regenerate questions and remove password
        elif request.form.get("action") == "reset":
            session["questions"] = generate_questions(session["num_questions"])
            return render_template("index.html",
                                   questions=session["questions"],
                                   num_questions=session["num_questions"],
                                   complexity=session["complexity"],
                                   password=None,
                                   entropy=None)

        # If Submit button was pressed we process answers in the text boxes
        elif request.form.get("action") == "submit":
            answers = {q["id"]: request.form.get(q["id"]) for q in questions}
            password = generate_password(answers, session['complexity'])
            entropy = calculate_entropy(password)
            return render_template("index.html",
                                   questions=session["questions"],
                                   num_questions=session["num_questions"],
                                   complexity=session["complexity"],
                                   password=password,
                                   entropy=entropy)

    return render_template("index.html",
                           questions=questions,
                           answers=None)

if __name__ == "__main__":
    app.run(debug=True)
