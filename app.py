from flask import Flask, render_template
from models import db, Job, User  # This "grabs" the code from models.py
from logic import get_match_analytics # This "grabs" the math from logic.py

app = Flask(__name__)
# ... (Configuration for your database goes here) ...

@app.route('/')
def home():
    # This tells Flask: "When someone visits the main page, show jobs.html"
    return render_template('jobs.html')

if __name__ == '__main__':
    app.run(debug=True)