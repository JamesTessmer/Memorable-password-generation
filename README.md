# Memorable Password Generator
## About
This project/tool was created for the Privacy Enhancing Tools course at Western Washington University (CSCI 497X/597X).
Our goal with this tool was to provide a local and easy way for users to create passwords. Our tool differs from existing password managers/generators because it personalizes the password and allows for varying lengths and levels of complexity.
We accomplish this by having a varied list of questions and randomly selecting a subset to display. The answers to these questions are pulled in and have pseudo-random changes made. For example answering three questions with `apple`, `orange`, and `banana` could result in a password like `4pPle=0ranGe-banANa`. The level of randomization and the number of questions asked is customizable.
As a rule of thumb a longer but simpler passphrase is harder to crack by brute force than a shorter, more complex passphrase, so if you want to create a stronger password we suggest that your first change be the number of questions.

## Setup
There are two options to set up this repository. The first is to use UV (recommended) or to use pip.
1. Start with either `uv sync` or `pip install -r dependencies.txt` to install the required packages.
2. There is also a required `.env` file where you will have to store a Flask app key. You can use the `.env_template` which has the expected variable name ready to be filled. You do not necessarily need to generate a random key if you are running and testing the app locally since any value will do. You could supply a key like `FLASK_APP_KEY="my super secret key"`.
3. Once all dependencies are installed you can run the app with `uv run python3 app.py` or `python3 app.py`.
4. The app serves the Flask's default port, so you can see it here `http://127.0.0.1:5000`.