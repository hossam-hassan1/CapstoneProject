from crypt import methods
from click import progressbar
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from app.helper import getClue, scavenger_hunts
from app.database.scavyQueries import get_game_list, get_game_from_code, get_clues, getClue, checkAnswer, user_login, create_user, create_game, log_play_count, checkProgress
from app.security import validatePassword

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# url string of class(route)
@app.route('/home')
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/log-in", methods=["GET", "POST"])
def login():
    error = ''
    if request.method == 'POST' and 'user' in request.form and 'password' in request.form:
        user = request.form["user"]
        password = request.form["password"]
        logged_in = user_login(user, password)
        if logged_in[0] == True:
            session['login'] = True
            session['username'] = user
            session['user_id'] = logged_in[2]
        else:
            error = logged_in[1]
    return render_template("login.html", error=error)

@app.route('/logout')
def logout():
    session['login'] = False
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route('/sign-up', methods=["POST", "GET"])
def create_account():
    message = ''
    validate = ''
    check = True
    if request.method == 'POST':
        email = request.form['email']
        user = request.form["user"]
        password = request.form["password"]
        confirm_password = request.form["password"]
        validate = validatePassword(password, confirm_password)
        check = validate[0]
        if validate[0] == True:
            create = create_user(email, user, password)
            if create[0] == True:
                message = create[1]
                logged_in = user_login(user, password)
                if logged_in[0] == True:
                    session['login'] = True
                    session['username'] = user
                    session['user_id'] = logged_in[2]
        else:
            validate = validate[1]
    return render_template("sign_up.html", check=check, validate=validate, message=message)

# renders privacy policy
@app.route('/privacy-policy')
def privacy():
    return render_template("privacy_policy.html")

# renders the play page with no game loaded
#  clue_id = -2  -> no game
@app.route('/play', methods=["POST", "GET"])
def noGame():
    if request.method == 'POST':
        game_code = request.form["game_code"]
        game = get_game_from_code(game_code)
        game_id = game[0][0]
        name = game[0][2]
        name = name.replace(" ", "_")
    
        return redirect(url_for("play", game=name, game_id=game_id))
    return render_template("play.html", clue_id=-2)

# renders a game with clues
# https://pythonbasics.org/flask-sessions/
@app.route('/play/<game>', methods=["POST", "GET"])
def play(game):
    game_id = request.args.get("game_id")
    print("Game ID: ", game_id)
    game = game.replace("_", " ")
    print(session)
    message = ""
    game_session = f'GAME + {game_id}'

    # game play counter 
    # implement passing var count from JS
    play_count = 2 
    log_play_count(play_count)

    # if there is an id in the game session continue
    # checks input name='nextClue' to go to next clue in play.html
    if game_session in session:
        print(True)
        if "nextClue" in request.form:
            id = session[game_session]
            #  get clues from database
            clues = get_clues(game_id)
            # get the clue the page is currently on
            clue = getClue(clues, id)
            input = request.form.get("answer_input")
            verify = checkAnswer(clue, input)
            print(verify)
            if verify == True:
                session[game_session] += 1
            else:
                message = "Sorry, try again!"
        # when nextClue is out of range (past final clue)
        # reset input in game complete automatically runs in play.html
        elif "reset" in request.form:
            session[game_session] = -1
        elif "restart" in request.form:
            session[game_session] = 0
    # otherwise game loads at the beginning
    else:
        print(False)
        session[game_session] = 0 
    # after the id is set in session set it in game
    id = session[game_session]
    #  get clues from database
    clues = get_clues(game_id)
    # get the clue the page is currently on
    clue = getClue(clues, id)
    # renders template with info needed to play game
    progress = checkProgress(clues, id)
    return render_template("play.html", game=game, id=id, clue_id=clue[0], prompt=clue[1], answer_type=clue[2], answer=clue[3], message=message, progress=progress)

@app.route('/search-games', methods=["POST", "GET"])
def search():

    if request.method == 'POST':
        game_code = request.form["game_code"]
        game = get_game_from_code(game_code)
        game_id = game[0][0]
        name = game[0][2]
        name = name.replace(" ", "_")
        return redirect(url_for("play", game=name, game_id=game_id))
    if "load_game" in request.form:
        game = request.form.get("load_game")
        game_id = request.form.get("game_id")
        game = game.replace(" ", "_")

        return redirect(url_for("play", game=game, game_id=game_id))
    
    scavenger_hunts = get_game_list("public")

    return render_template("search.html", scavenger_hunts=scavenger_hunts)

# create_game(user_id, game_title, game_description, privacy_level, gps_required, camera_required)
@app.route('/create-game', methods=["POST", "GET"])
def game_create():
    message = ''
    if request.method == 'POST':
        user_id = session['user_id']
        game_title = request.form["game_title"]
        game_description = request.form["game_description"]
        privacy_level = request.form["privacy_level"]
        try:
            camera_required = request.form["camera_required"]
        except:
            camera_required = 'false'
        try:
            gps_required = request.form["gps_required"]
        except:
            gps_required = 'false'
        # print(f'{user_id, game_title, game_description, privacy_level, gps_required, camera_required}')
        message = create_game(user_id, game_title, game_description, privacy_level, gps_required, camera_required)
        # return redirect(url_for("clues", username='test', game='game'))
    return render_template("create_game.html", message=message)

@app.route('/<username>/games/<game>', methods=["POST", "GET"])
def clues(username, game):

    return render_template("add_clues.html")

# https://www.geeksforgeeks.org/python-404-error-handling-in-flask/#:~:text=A%20404%20Error%20is%20showed,the%20default%20Ugly%20Error%20page.
@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
# defining function
  return render_template("404.html")

if __name__ == "__main__":
    # debug means that if there are errors it will display on the webserver
    app.run(debug=True)