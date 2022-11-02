# -- Python function per page:


import mysql.connector
import random

# create_game(1, "test title", "test description", "public", "true", "false")


# -- play/search.html


#     -- get_game() - a get query to find game by game code from Games Tables


# -- sign_up.html
def create_query(query):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            database="scavyDB",
            user="root",
            passwd="pass"
        )
        mycursor = mydb.cursor()
        mycursor.execute(query)
        mydb.commit()
        return mycursor.lastrowid
    except Exception as err:
        print(f"Error Occured: {err}\nExiting program...")
        quit()

def search_query(query):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            database="scavyDB",
            user="root",
            passwd="pass"
        )
        mycursor = mydb.cursor()
        mycursor.execute(query)
        query_result = mycursor.fetchall()
        return query_result
    except Exception as err:
        print(f"Error Occured: {err}\nExiting program...")
        quit()


# create_user() - an insert query into Users Table  (email, user_name, password)
def create_user(email, username, password):
    insert = f"""
        INSERT INTO Users (email, username, password)
        VALUES ("{email}", "{username}", SHA2("{password}",256));"""
    message = "User added!"
    created = False
    try:
        create_query(insert)
        message = "User added!"
        created = True
    except:
        check_username = f'SELECT user_id FROM Users WHERE username = "{username}";'
        user_exists = search_query(check_username)
        check_email = f'SELECT user_id FROM Users WHERE email = "{email}";'
        email_exists = search_query(check_email)
        if len(user_exists) == 1 and len(email_exists) == 1:
            message = 'Username and email already exists.'
        elif len(user_exists) == 1:
            message = 'Username already exists.'
        else:
            message = 'Email already exists.'
    # else:
    #     message = 'Unknown Error Occurred.'
    return created, message

# user = create_user('guest@guest.com', 'guest', 'Guest!23')
# print(user)

# -- login.html (Users Table)

# get_user() - a get query to validate user exists and return user account info 
#  (associated games created) (email, user_name, password)
def get_user(username, password):
    select_user = f"""
    SELECT user_id FROM Users WHERE username = "{username}" AND password = "{password}";
    """
    result = search_query(select_user)
    if len(result) == 1:
        select_games = f"""
        SELECT game_title FROM Games WHERE user_id = 1;
        """
        result = search_query(select_games)
        print(f"{username}'s Games:")
        print(result)
        return result
    else:
        print("user does not exit")

def user_login(username, password):
    select_user = f"""
    SELECT user_id FROM Users WHERE username = "{username}" AND password = SHA2("{password}",256);
    """
    user = search_query(select_user)
    user_id = 0
    logged_in = False
    error = ''
    if len(user) == 1:
        logged_in = True
        for record in user:
            for id in record:
                user_id = id
    else:
        check_username = f'SELECT user_id FROM Users WHERE username = "{username}";'
        result = search_query(check_username)
        if len(result) == 1:
            error = 'Password is invalid.'
        else:
            error = 'Username does not match any records.'
    return logged_in, error, user_id


# logged_in = user_login('test', 'testdfsd')
# print(logged_in[0])
# print(logged_in[1])


# create_game.html

def generate_game_code(game_title):
    generate = True
    while(generate):
        first = game_title[:6]
        code = ''
        for i in range(4):
            i = random.randint(0,9)
            code += str(i)
        check_code = f'SELECT game_code FROM Games WHERE game_code = SHA2("{first + code}", 256);'
        code_exists = search_query(check_code)
        if len(code_exists) == 0:
            generate = False
    return first + code
code = generate_game_code("Miz")
print(code)

#  create_game() - an insert query into Games, Clues, and Locations Tables
def create_game(user_id, game_title, game_description, privacy_level, gps_required, camera_required):
    game_code = generate_game_code(game_title)
    insert = f"""
    INSERT INTO Games (user_id, game_title, game_description, privacy_level, gps_required, camera_required, game_code)
    VALUES ({user_id}, "{game_title}", "{game_description}", "{privacy_level}", "{gps_required}", "{camera_required}", SHA2("{game_code}", 256));
    """
    message = ''
    created = False
    game_id = 0
    # try:
    try:
        game_id = create_query(insert)
        created = True
        message = f"Game: '{game_title}' has been created!"
    except:
        message = 'Game could not be created.'
    return created, message, game_id

def edit_game(game_id, game_title, game_description, privacy_level, gps_required, camera_required):
    update = f"""
        UPDATE Games
        SET game_title="{game_title}", game_description="{game_description}", privacy_level="{privacy_level}", gps_required="{gps_required}", camera_required="{camera_required}"
        WHERE game_id = {game_id};
    """
    message = ''
    # try:
    try:
        game_id = create_query(update)
        message = f"Game: '{game_title}' has been updated!"
    except:
        message = 'Game could not be updated.'
    return message

#     -- get_game_list() - a get query to list all games from Games Tables
def get_game_list(privacy_level):
    list_all_games = f"SELECT * FROM Games WHERE privacy_level = '{privacy_level}';"
    result = search_query(list_all_games)
    games = []
    for record in result:
        # items = []
        # for item in record:
        #     items.append(item)
        games.append(record)
    return games

# games = get_game_list("public")
# for game in games:
#     print(game[2])

#     -- get_game_by_title() - a get query to list a game by game title from Games Table
def get_game_by_title(game_title, privacy_level):
    games_by_title = f"SELECT game_title FROM GAMES where game_title = '{game_title}' AND privacy_level = '{privacy_level}';"
    result = search_query(games_by_title)
    return result

def get_game_by_id(game_id):
    game = f"SELECT * FROM GAMES where game_id = '{game_id}';"
    result = search_query(game)
    return result

#     -- get_game_by_descr() - a get query to list a game by game description from Games Table
def get_game_location(game_description, privacy_level):
    games_by_description = f"SELECT game_title FROM GAMES where game_description = '{game_description}' AND privacy_level = '{privacy_level}';"
    result = search_query(games_by_description)
    for game in result:
        print(game)
    return result
# Are we meaning this function to search any words in the description? 
# We could do a split by space into a list of the words searched to check if any word is in the list.


#     -- get_most_played_games() - a get query to list the most played games from Games Tables (not sure if we are still doing this)


# -- play.html/GAME

#     -- get_game_details() - a get query to retrieve all game details based on game code from Games, Clues, and Locations Tables.
def get_game_from_code(game):
    game_details = f"SELECT * FROM Games WHERE game_code = SHA2('{game}', 256);"
    code_message = ""
    exists = False
    result = search_query(game_details)
    if len(result) == 1:
        exists = True
        game = []
        for record in result:
            game.append(record)
        game_id = game[0][0]
        name = game[0][2]
        name = name.replace(" ", "_")
    else:
        exists = False
        name = False
        game_id = False
        code_message = "Game code does not exist."
    return exists, name, game_id, code_message

def get_games_from_user(user_id):
    user_games = f"SELECT * FROM Games WHERE user_id = {user_id};"
    result = search_query(user_games)
    games = []
    for record in result:
        games.append(record)
    return games

# game = get_game_from_code(1776)
# print(game)

def get_clues(game_id):
    clues_list = f"SELECT * FROM Clues WHERE game_id = '{ game_id }';"
    result = search_query(clues_list)
    clues = []
    for record in result:
        clues.append(record)
    return clues

# print(get_clues(1))

def check_privacy(game_id):
    privacy_query = f"SELECT privacy_level FROM Games WHERE game_id = '{game_id}';"
    result = search_query(privacy_query)
    privacy = ''
    for record in result:
        for level in record: 
            privacy = level
    print(privacy)
    return privacy

check_privacy(1)
# clues = get_clues(1)

# clue = clues[0]

# print(clue[2])

def getClue(clues, id):
    total = len(clues)
    if id < total:
        clue = clues[id] 
        clue_id = id + 1
        prompt = clue[2]
        answer_type = clue[5]
        answer = clue[6]
    else:
        clue_id = -1
        prompt = f"Congrats! You have completed {game}."
        answer_type = ""
        answer = ""
    return clue_id, prompt, answer_type, answer

def check_radius(radius):
    pass

def checkAnswer(clue, input):
    answer_type = clue[2]
    answer = clue[3]
    correct = False
    if answer_type == 'text':
        if answer.lower() == input.lower():
            correct = True
    elif answer_type == 'coordinates':
        # input = javascrip check-in
        # check_radius()
        correct = True
    return correct

def checkProgress(clues, id):
    total = len(clues)
    completion = (id/total) * 100
    return completion

# completion = checkProgress(clues, 1)
# print(completion)

def check_form_boxes(privacy_level, camera_required, gps_required):
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
    return public_radio, private_radio, camera_box, gps_box

def load_edit_form(game_id):
    game = get_game_by_id(game_id)
    game_description = game[0][3]
    game_title = game[0][2]
    boxes = check_form_boxes(game[0][5], game[0][6], game[0][7])
    public_radio = boxes[0]
    private_radio = boxes[1]
    camera_box = boxes[2]
    gps_box = boxes[3]
    return game_title, game_description, public_radio, private_radio, gps_box, camera_box

def save_game_form(game_id, request):
    game = get_game_by_id(game_id)
    game_title = request.form["game_title"]
    if game_title == '': 
        game_title = game[0][2]
    game_description = request.form["game_description"]
    if game_description == '':
        game_description = game[0][3]
    privacy_level = request.form["privacy_level"]
    try:
        camera_required = request.form["camera_required"]
    except:
        camera_required = 'false'
    try:
        gps_required = request.form["gps_required"]
    except:
        gps_required = 'false'
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
    message = edit_game(game_id, game_title, game_description, privacy_level, gps_required, camera_required)
    return game_title, game_description, public_radio, private_radio, gps_box, camera_box, message