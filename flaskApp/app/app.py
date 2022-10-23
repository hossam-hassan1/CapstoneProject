from crypt import methods
from flask import Flask, render_template, request, redirect, url_for
# from app.helper import getClue, scavenger_hunts
from app.database.scavyQueries import get_game_list, get_clues, getClue

app = Flask(__name__)

# sets session variable for game to track current clue
game_session = {'id':0}

# url string of class(route)
@app.route('/home')
@app.route('/')
# function for that route
def index():
    return render_template('index.html')

@app.route("/log-in", methods=["GET"])
def login():
    # requires the user to enter data
    # if request.method == "POST":
    # gives us the "userName" data from the HTML page
    #     user = request.form["userName"]
    #     return redirect(url_for("user", user=user))
    # else:
    return render_template("login.html")

# @app.route("/<user>")
# def user(user):
#     return f"<h1>Hello {user}</h1>"

@app.route('/sign-up')
def create_account():
    return render_template("sign_up.html")

# renders privacy policy
@app.route('/privacy-policy')
def privacy():
    return render_template("privacy_policy.html")

# renders the play page with no game loaded
#  clue_id = -2  -> no game
@app.route('/play')
def noGame():
    return render_template("play.html", clue_id=-2)

# renders a game with clues
# https://pythonbasics.org/flask-sessions/
@app.route('/play/<game>', methods=["POST", "GET"])
def play(game):
    game_id = request.args.get("game_id")
    game = game.replace("_", " ")
    # if there is an id in the game session continue
    if 'id' in game_session:
        # checks name = nextClue of input to next clue in play.html
        if "nextClue" in request.form:
            game_session['id'] += 1
        # when next is out of range (past final clue)
        # reset input in game complete automatically runs in play.html
        elif "reset" in request.form:
            game_session['id'] = -1
        # otherwise game loads at the beginning
        else:    
            game_session['id'] = 0
        # after the is is set in session set it in game
        id = game_session['id']
        #  get clues from database
        clues = get_clues(game_id)

        clue = getClue(clues, id)
        # renders template with info needed to play game
        return render_template("play.html", game=game, id=id, clue_id=clue[0], prompt=clue[1], answer_type=clue[2], answer=clue[3])

@app.route('/search-games', methods=["POST", "GET"])
def search():
    if "load_game" in request.form:
        game = request.form.get("load_game")
        game_id = request.form.get("game_id")
        game = game.replace(" ", "_")
        return redirect(url_for("play", game=game, game_id=game_id))
    scavenger_hunts = get_game_list("public")
    return render_template("search.html", scavenger_hunts=scavenger_hunts)

@app.route('/create-game')
def create_game():
    return render_template("create_game.html")

# https://www.geeksforgeeks.org/python-404-error-handling-in-flask/#:~:text=A%20404%20Error%20is%20showed,the%20default%20Ugly%20Error%20page.
@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
# defining function
  return render_template("404.html")

if __name__ == "__main__":
    # debug means that if there are errors it will display on the webserver
    app.run(debug=True)