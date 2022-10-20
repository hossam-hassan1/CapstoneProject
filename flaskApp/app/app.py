from crypt import methods        
from flask import Flask, render_template, request, redirect, url_for, flash
from app.helper import scavenger_hunts, getClue
from app.static.scripts.forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user
# Add login feacher: https://www.youtube.com/watch?v=CSHx6eCkmv0
app = Flask(__name__)
# Config key for Login cookie, eleminate modifying cookies
# A random 16 digit byte using import secrets
app.config['SECRET_KEY'] = '5edbf69ea6767da4941b5057905b30cd'    
bcrypt = Bcrypt(app)
#login_manager = LoginManager(app)
# url string of class(route)
@app.route('/home')
@app.route('/')
# function for that route
def index():
    return render_template('index.html')

@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # if successfull login
        #user = User.query.filter_by(email = form.email.data).first()
        # password from db (user.password)
        # if user and bcrypt.check_password_hash(user.password , form.password.data):
        #     login_user(user, remember=form.remember.data)
        #     return redirect(url_for('index'))
        # else:
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template("login.html", form=form)
# @app.route("/login", methods=["POST", "GET"])
# def login():
#     # requires the user to enter data
#     if request.method == "POST":
#     # gives us the "userName" data from the HTML page
#         user = request.form["userName"]
#         return redirect(url_for("user", user=user))
#     else:
#         return render_template("login.html")

@app.route("/<user>")
def user(user):
    return f"<h1>Hello {user}</h1>"

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    form = RegistrationForm()
    if form.validate_on_submit():
        # turns password into hashed password
        # hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utc-8')
        # Add user to the database
        # user = Users(username=form.username.data, email=form.email.data, password=hashed_password)
        # db.session.add(user)
        # db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template("create_account.html", form=form)

@app.route('/privacy')
def privacy():
    return render_template("privacy.html")

@app.route('/play')
def noGame():
    return render_template("play.html", clue_id=-2)

@app.route('/play/<game>/<int:id>')
def play(game, id):
    clue = getClue(scavenger_hunts, game, id)
    return render_template("play.html", game=game, id=id, clue_id=clue[0], prompt=clue[1], coordinates=clue[2], answer=clue[3])

@app.route('/search')
def search():
  return render_template("search.html", scavenger_hunts=scavenger_hunts)

@app.route('/create_game')
def create_game():
    return render_template("create_game.html")

@app.route('/geolocation')
def geolocation():
    return render_template("geolocation.html")

# https://www.geeksforgeeks.org/python-404-error-handling-in-flask/#:~:text=A%20404%20Error%20is%20showed,the%20default%20Ugly%20Error%20page.
@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
# defining function
  return render_template("404.html")

if __name__ == "__main__":
    # debug means that if there are errors it will display on the webserver
    app.run(debug=True)