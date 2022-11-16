from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
# from app.helper import getClue, scavenger_hunts
from app.database.scavyQueries import get_game_list, get_game_from_code, delete_game, get_clues, getClue, checkAnswer, checkProgress, user_login, create_user, create_game, get_games_from_user, check_privacy, get_game_by_id, edit_game, load_edit_form, save_game_form, get_game_by_title, add_clue, delete_clue, move_clue, get_clue, edit_clue, delete_account, find_play_count, log_play_count
from app.security import validatePassword
from app import app

#app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# url string of class(route)
@app.route('/home')
@app.route("/")
def index():
    return render_template('index.html')

# def login_form():
#     print(session)
#     error = ''
#     if request.method == 'POST' and 'user' in request.form and 'password' in request.form:
#         user = request.form["user"]
#         password = request.form["password"]
#         logged_in = user_login(user, password)
#         if logged_in[0] == True:
#             session['login'] = True
#             session['username'] = user
#             session['user_id'] = logged_in[2]
#             error = logged_in[1]
#         else:
#             error = logged_in[1]
#     return error

# @app.route("/log-in", methods=["GET", "POST"])
# def login():
#     if 'login' not in session or session['login'] == False:
#         pass
#     elif session['login'] == True:
#          return redirect(url_for('account'))
#     error = login_form()
#     if error == False:
#         return redirect(url_for("account"))
#     return render_template("login.html", error=error)

# @app.route('/logout')
# def logout():
#     if 'login' not in session or session['login'] == False:
#         return redirect(url_for('login'))
#     session['login'] = False
#     session.pop('username', None)
#     session.pop('user_id', None)
#     return redirect(url_for('login'))


# @app.route('/sign-up', methods=["POST", "GET"])
# def create_account():
#     if 'login' not in session or session['login'] == False:
#         pass
#     elif session['login'] == True:
#          return redirect(url_for('account'))
#     message = ''
#     validate = ''
#     check = True
#     if request.method == 'POST':
#         email = request.form['email']
#         user = request.form["user"]
#         password = request.form["password"]
#         confirm_password = request.form["password"]
#         validate = validatePassword(password, confirm_password)
#         check = validate[0]
#         if validate[0] == True:
#             create = create_user(email, user, password)
#             if create[0] == True:
#                 message = create[1]
#                 logged_in = user_login(user, password)
#                 if logged_in[0] == True:
#                     session['login'] = True
#                     session['username'] = user
#                     session['user_id'] = logged_in[2]
#                 return redirect(url_for("account"))
#         else:
#             validate = validate[1]
#     return render_template("sign_up.html", check=check, validate=validate, message=message)

# @app.route('/account', methods=["POST", "GET"])
# def account():
#     if 'login' not in session:
#         return redirect(url_for('create_account'))
#     elif session['login'] == False:
#         return redirect(url_for('login'))
#     else:
#         pass
#     message = ''
#     if 'confirm_delete_account' in request.form:
#         user_id = request.form["user_id"]
#         delete_account(game_id)
#         return redirect(url_for("index"))
#     if 'delete_game' in request.form:
#         user_id = session["user_id"]
#         message = delete_game(game_id)
#     if 'load_edit' in request.form:
#         game_id = request.form["game_id"]
#         game = get_game_by_id(game_id)
#         name = game[2].replace(" ", "_")
#         return redirect(url_for("game_edit", game=name))
#         # return render_template("create_game.html", mode='edit', read='readonly', disabled='disabled', message='', title_placeholder=game[0], description_placeholder=game[1], public_radio=game[2], private_radio=game[3], gps_box=game[4], camera_box=game[5], game_id=game_id)
#     username = session['username']
#     user_id = session['user_id']
#     scavenger_hunts = get_games_from_user(user_id)
#     return render_template("account.html", username=username, scavenger_hunts=scavenger_hunts, message=message)

#     # renders privacy policy
#     @app.route('/privacy-policy')
#     def privacy():
#         return render_template("privacy_policy.html")

#     # # renders the play page with no game loaded
#     # #  clue_id = -2  -> no game
#     @app.route('/play', methods=["POST", "GET"])
#     def noGame():
#         code_error=""
#         code_prompt="Alread have a game code? Enter to play."
#         if request.method == 'POST':
#             game_code = request.form["game_code"]
#             game = get_game_from_code(game_code)
#             if game[0] == True:
#                 session[f'GAME{game[2]}'] = 0
#                 return redirect(url_for("play", game=game[1]))
#             elif game[1] == False:
#                 return render_template("play.html", clue_id=-2, code_prompt=code_prompt, code_error=game[3]) 
#         return render_template("play.html", code_error=code_error, code_prompt=code_prompt, clue_id=-2)

# # renders a game with clues
# # https://pythonbasics.org/flask-sessions/
# @app.route('/play/<game>', methods=["POST", "GET"])
# def play(game):
#     game = game.replace("_", " ")
#     game_id = get_game_by_title(game)
#     game_session = f'GAME{game_id}'
#     message = ""
#     game_privacy = check_privacy(game_id)

#     # game play counter 
#     print("Game ID: ", game_id)
#     play_count = find_play_count(game_id)
#     print("play count: ", play_count)

#     if game_privacy == "public":
#         pass
#     elif game_privacy == 'private':
#         if game_session not in session:
#             code_prompt = f"{game} requires a code to play."
#             code_error = ""
#             if request.method == 'POST':
#                 game_code = request.form["game_code"]
#                 load_game = get_game_from_code(game_code)
#                 if load_game[0] == True:
#                     session[f'GAME{load_game[2]}'] = 0
#                     return redirect(url_for("play", game=load_game[1]))
#                 if load_game[0] == False:
#                     code_error = load_game[3]
#             return render_template("play.html", game=game, privacy=game_privacy, code_error=code_error, code_prompt=code_prompt)
#         else:
#             pass
#     # if there is an id in the game session continue
#     # checks input name='nextClue' to go to next clue in play.html
    if game_session in session:
        print(True)
        
        total_count = play_count + 1
        print("total count: ", total_count)

        log_play_count(total_count, game_id)

        if "nextClue" in request.form:
            id = session[game_session]
            #  get clues from database
            clues = get_clues(game_id)
            # get the clue the page is currently on
            clue = getClue(clues, id, game)
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
        session[game_session] = 0 
    # after the id is set in session set it in game
    id = session[game_session]
    #  get clues from database
    clues = get_clues(game_id)
    # get the clue the page is currently on
    clue = getClue(clues, id, game)
    # renders template with info needed to play game
    progress = checkProgress(clues, id)
    return render_template("play.html", game=game, id=id, clue_id=clue[0], prompt=clue[1], answer_type=clue[2], answer=clue[3], message=message, progress=progress, play_count=play_count)

    @app.route('/search-games', methods=["POST", "GET"])
    def search():
        scavenger_hunts = get_game_list("public")
        code_error=""
        code_prompt="Alread have a game code? Enter to play."
        if "load_game" in request.form:
            game = request.form.get("load_game")
            game_id = request.form.get("game_id")
            session['load_game'] = game_id
            game = game.replace(" ", "_")
            return redirect(url_for("play", game=game))
        elif request.method == 'POST':
            game_code = request.form["game_code"]
            game = get_game_from_code(game_code)
            if game[0] == True:
                session[f'GAME{game[2]}'] = 0
                return redirect(url_for("play", game=game[1]))
            elif game[1] == False:
                return render_template("search.html", scavenger_hunts=scavenger_hunts, code_error=game[3], code_prompt=code_prompt)
        return render_template("search.html", scavenger_hunts=scavenger_hunts, code_error=code_error, code_prompt=code_prompt)

    # create_game(user_id, game_title, game_description, privacy_level, gps_required, camera_required)
    @app.route('/create-game', methods=["POST", "GET"])
    def game_create():
        if 'login' not in session or session['login'] == False:
            error = login_form()
            if error == False:
                return redirect(url_for("game_create"))
            return render_template("create_game.html", error=error)
        elif session['login'] == True:
            user_id = session['user_id'] 
        message = ''
        if 'create_game' in request.form:
            mode = 'create'
            game_id = 0
            game = save_game_form(game_id, user_id, request, mode)
            print(game)
            if game[0] != False:
                return redirect(url_for("game_edit", game=game[0]))
            else:
                message = game[1]
        return render_template("create_game.html", mode='create', read='', message=message, disabled='', title_placeholder='What is your game called?', description_placeholder='Tell us about your game.', public_radio='', private_radio='checked', gps_box='', camera_box='')

    @app.route('/edit-game/<game>', methods=["POST", "GET"])
    def game_edit(game):
        game_id = get_game_by_title(game.replace("_", " "))
        game = load_edit_form(game_id)
        clues = get_clues(game_id)
        clue_message = ''
        if 'login' not in session or session['login'] == False:
            error = login_form()
            if error == False:
                return redirect(url_for("game_edit", game=game[0]))
            else:
                return render_template("create_game.html", error=error)
        elif session['login'] == True:
            user_creator = get_game_by_id(game_id)[1]
            user_id = session['user_id'] 
            if user_creator != user_id:
                user_creator = False
                return render_template("create_game.html", user_creator=user_creator)
        if 'add_clue' in request.form:
            prompt_text = request.form["prompt_text"]
            answer_type = request.form["answer_type"]
            answer = request.form["answer"]
            clue = add_clue(game_id, prompt_text, answer_type, answer)
            if clue[0] != False:   
                return redirect(url_for("game_edit", game=game[0]))   
            else:
                clue_message = clue[1]
        if 'edit_clue' in request.form:
            clue_id = request.form["edit_clue"]
            clue = get_clue(clue_id)
            prompt_text = request.form["edit_prompt_text"]
            if prompt_text == '':
                prompt_text = clue[3]
            answer_type = request.form["edit_answer_type"]
            answer = request.form["edit_answer"]
            if answer == '':
                answer = clue[7]
            clue = edit_clue(clue_id, prompt_text, answer_type, answer)
            return redirect(url_for("game_edit", game=game[0])) 
        if 'delete_clue' in request.form:
            clue_id = request.form["delete_clue"]
            clue_message = delete_clue(clue_id, game_id)
            return redirect(url_for("game_edit", game=game[0]))
        if 'move_clue_up' in request.form:
            clue_id = request.form["move_clue_up"]
            clue_message = move_clue(clue_id, game_id, 'up')
            return redirect(url_for("game_edit", game=game[0]))
        if 'move_clue_down' in request.form:
            clue_id = request.form["move_clue_down"]
            clue_message = move_clue(clue_id, game_id, 'down')
            return redirect(url_for("game_edit", game=game[0]))
        if 'save_game' in request.form:
            mode = 'save'
            game_id = request.form["game_id"]
            game = save_game_form(game_id, user_id, request, mode)
            return redirect(url_for("game_edit", game=game[0]))
        if 'edit_game' in request.form:
            mode = 'edit'
            game_id = request.form["game_id"]
            return render_template("create_game.html", clues=clues, mode='save', read='', disabled='', message='', title_placeholder=game[0], description_placeholder=game[1], public_radio=game[2], private_radio=game[3], gps_box=game[4], camera_box=game[5], game_id=game_id)
        return render_template("create_game.html", clue_message=clue_message, clues=clues, mode='edit', read='readonly', disabled='disabled', message='', title_placeholder=game[0], description_placeholder=game[1], public_radio=game[2], private_radio=game[3], gps_box=game[4], camera_box=game[5], game_id=game_id)


@app.route('/geolocation')
def geolocation():
    return render_template("geolocation.html")



# https://www.geeksforgeeks.org/python-404-error-handling-in-flask/#:~:text=A%20404%20Error%20is%20showed,the%20default%20Ugly%20Error%20page.
@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
# defining function
  return render_template("404.html")


