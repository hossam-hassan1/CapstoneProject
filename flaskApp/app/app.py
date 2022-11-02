from crypt import methods
from click import progressbar
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
# from app.helper import getClue, scavenger_hunts
from app.database.scavyQueries import get_game_list, get_game_from_code, get_clues, getClue, checkAnswer, checkProgress, user_login, create_user, create_game, get_games_from_user, check_privacy, get_game_by_id, edit_game, load_edit_form, save_game_form
from app.security import validatePassword

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# url string of class(route)
@app.route('/home')
@app.route('/')
# function for that route
def index():
    return render_template('index.html')

@app.route("/log-in", methods=["GET", "POST"])
def login():
    print(session)
    error = ''
    if request.method == 'POST' and 'user' in request.form and 'password' in request.form:
        user = request.form["user"]
        password = request.form["password"]
        logged_in = user_login(user, password)
        if logged_in[0] == True:
            session['login'] = True
            session['username'] = user
            session['user_id'] = logged_in[2]
            return redirect(url_for("account"))
        else:
            error = logged_in[1]
    return render_template("login.html", error=error)

@app.route('/logout')
def logout():
    if session['login'] == False:
        return redirect(url_for('login'))
    session['login'] = False
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route('/sign-up', methods=["POST", "GET"])
def create_account():
    if session['login'] == True:
        return redirect(url_for('account'))
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
                return redirect(url_for("account"))
        else:
            validate = validate[1]
    return render_template("sign_up.html", check=check, validate=validate, message=message)

@app.route('/account', methods=["POST", "GET"])
def account():
    if session['login'] == False:
        return redirect(url_for('login'))
    username = session['username']
    user_id = session['user_id']
    scavenger_hunts = get_games_from_user(user_id)
    if 'load_edit' in request.form:
        game_id = request.form["game_id"]
        game = load_edit_form(game_id)
        return render_template("create_game.html", mode='edit', read='readonly', disabled='disabled', message='', title_placeholder=game[0], description_placeholder=game[1], public_radio=game[2], private_radio=game[3], gps_box=game[4], camera_box=game[5], game_id=game_id)
    return render_template("account.html", username=username, scavenger_hunts=scavenger_hunts)

# renders privacy policy
@app.route('/privacy-policy')
def privacy():
    return render_template("privacy_policy.html")

# renders the play page with no game loaded
#  clue_id = -2  -> no game
@app.route('/play', methods=["POST", "GET"])
def noGame():
    code_error=""
    code_prompt="Alread have a game code? Enter to play."
    if request.method == 'POST':
        game_code = request.form["game_code"]
        game = get_game_from_code(game_code)
        
        if game[0] == True:
            session[f'GAME{game[2]}'] = 0
            return redirect(url_for("play", game=game[1], game_id=game[2]))
        elif game[1] == False:
            return render_template("play.html", clue_id=-2, code_prompt=code_prompt, code_error=game[3]) 
    return render_template("play.html", code_error=code_error, code_prompt=code_prompt, clue_id=-2)

# renders a game with clues
# https://pythonbasics.org/flask-sessions/
@app.route('/play/<game>', methods=["POST", "GET"])
def play(game):
    game_id = request.args.get("game_id")
    game_session = f'GAME{game_id}'
    game = game.replace("_", " ")
    print(session)
    message = ""
    game_privacy = check_privacy(game_id)
    if game_privacy == "public":
        pass
    elif game_privacy == 'private':
        if game_session not in session:
            code_prompt = f"{game} requires a code to play."
            code_error = ""
            if request.method == 'POST':
                game_code = request.form["game_code"]
                load_game = get_game_from_code(game_code)
                if load_game[0] == True:
                    session[f'GAME{load_game[2]}'] = 0
                    return redirect(url_for("play", game=load_game[1], game_id=load_game[2]))
                if load_game[0] == False:
                    code_error = load_game[3]
            return render_template("play.html", game=game, privacy=game_privacy, code_error=code_error, code_prompt=code_prompt)
        else:
            pass
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
    scavenger_hunts = get_game_list("public")
    code_error=""
    code_prompt="Alread have a game code? Enter to play."
    if "load_game" in request.form:
        game = request.form.get("load_game")
        game_id = request.form.get("game_id")
        game = game.replace(" ", "_")
        return redirect(url_for("play", game=game, game_id=game_id))
    elif request.method == 'POST':
        game_code = request.form["game_code"]
        game = get_game_from_code(game_code)
        if game[0] == True:
            session[f'GAME{game[2]}'] = 0
            return redirect(url_for("play", game=game[1], game_id=game[2]))
        elif game[1] == False:
            return render_template("search.html", scavenger_hunts=scavenger_hunts, code_error=game[3], code_prompt=code_prompt)
    return render_template("search.html", scavenger_hunts=scavenger_hunts, code_error=code_error, code_prompt=code_prompt)

# create_game(user_id, game_title, game_description, privacy_level, gps_required, camera_required)
@app.route('/create-game', methods=["POST", "GET"])
def game_create():
    user_id = session['user_id']
    if 'save_game' in request.form:
        game_id = request.form["game_id"]
        game = save_game_form(game_id, request)
        return render_template("create_game.html", mode='edit', read='readonly', disabled='disabled', message=game[6], title_placeholder=game[0], description_placeholder=game[1], public_radio=game[2], private_radio=game[3], gps_box=game[4], camera_box=game[5], game_id=game_id)
    if 'edit_game' in request.form:
        game_id = request.form["game_id"]
        game = load_edit_form(game_id)
        return render_template("create_game.html", mode='save', read='', disabled='', message='', title_placeholder=game[0], description_placeholder=game[1], public_radio=game[2], private_radio=game[3], gps_box=game[4], camera_box=game[5], game_id=game_id)
    if 'create_game' in request.form:
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
        if game_title != '' and game_description != '':
            message = create_game(user_id, game_title, game_description, privacy_level, gps_required, camera_required)
        else:
            message = 'Please fill out missing form fields.'
        if message[0] == True:
            if privacy_level == 'public':
                public_radio = 'checked'
                private_radio = ''
            else:
                public_radio = ''
                private_radio = 'checked'
            if camera_required == 'true':
                camera_box = 'checked'
            else:
                camera_box = ''
            if gps_required == 'true':
                gps_box = 'checked'
            else:
                gps_box = ''
            return render_template("create_game.html", mode='edit', read='readonly', disabled='disabled', message=message[1], title_placeholder=game_title, description_placeholder=game_description, public_radio=public_radio, private_radio=private_radio, gps_box=gps_box, camera_box=camera_box, game_id=message[2])
        elif message[0] == False:
            return render_template("create_game.html", mode="", read='', disabled='', message=message[1], title_placeholder='What is your game called?', description_placeholder='Tell us about your game.', public_radio=public_radio, private_radio='checked', gps_box='', camera_box='')
        # return redirect(url_for("account"))
    return render_template("create_game.html", mode='', read='', message='', disabled='', title_placeholder='What is your game called?', description_placeholder='Tell us about your game.', public_radio='', private_radio='checked', gps_box='', camera_box='')

# https://www.geeksforgeeks.org/python-404-error-handling-in-flask/#:~:text=A%20404%20Error%20is%20showed,the%20default%20Ugly%20Error%20page.
@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
# defining function
  return render_template("404.html")

if __name__ == "__main__":
    # debug means that if there are errors it will display on the webserver
    app.run(debug=True)