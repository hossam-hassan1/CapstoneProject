from flask import Flask, render_template, request, redirect, url_for
from app.helper import scavenger_hunts, getClue

app = Flask(__name__)

# url string of class(route)
@app.route('/home')
@app.route('/')
# function for that route
def index():
    return render_template('index.html')

@app.route("/login", methods=["POST", "GET"])
def login():
    # requires the user to enter data
    if request.method == "POST":
    # gives us the "userName" data from the HTML page
        user = request.form["userName"]
        return redirect(url_for("user", user=user))
    else:
        return render_template("login.html")

@app.route("/<user>")
def user(user):
    return f"<h1>Hello {user}</h1>"

@app.route('/create_account')
def create_account():
    return render_template("create_account.html")

@app.route('/privacy')
def privacy():
    return render_template("privacy.html")

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

if __name__ == "__main__":
    # debug means that if there are errors it will display on the webserver
    app.run(debug=True)