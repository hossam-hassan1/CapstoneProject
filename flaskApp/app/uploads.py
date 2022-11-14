import os
from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/Users/kennabogue/Documents/MIZZOU/22_FALL/INFOTC_4970_Capstone/Learning Flask/FlaskIdeas/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'






@app.route('/')
def index():
  return render_template("home.html")

@app.route('/home')
def home():
  return render_template("home.html")

@app.route("/explore")
def explore():
  return render_template("explore.html")


@app.route("/make")
def make():
  return render_template("make.html")


@app.route("/play")
def play():
  return render_template("play.html")