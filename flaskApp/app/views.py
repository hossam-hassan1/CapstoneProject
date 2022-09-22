from flask import render_template
from app import app

@app.route('/')
def home():
    return "Hello World"

@app.route('/template')
def template():
    return render_template('index.html')
