# -- Python function per page:


import mysql.connector

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
    except Exception as err:
        # print(f"Error Occured: {err}\nExiting program...")
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
    result = search_query(select_user)
    logged_in = False
    error = ''
    if len(result) == 1:
        logged_in = True
    else:
        check_username = f'SELECT user_id FROM Users WHERE username = "{username}";'
        result = search_query(check_username)
        if len(result) == 1:
            error = 'Password is invalid.'
        else:
            error = 'Username does not match any records.'
    return logged_in, error


# logged_in = user_login('test', 'testdfsd')
# print(logged_in[0])
# print(logged_in[1])


# create_game.html

#  create_game() - an insert query into Games, Clues, and Locations Tables
def create_game(user_id, game_title, game_description, privacy_level, gps_required, camera_required):
    insert = f"""
    INSERT INTO Games (user_id, game_title, game_description, privacy_level, gps_required, camera_required)
    VALUES ({user_id}, "{game_title}", "{game_description}", "{privacy_level}", "{gps_required}", "{camera_required}");
    """
    success = "Game created!"
    create_query(insert, success)

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

games = get_game_list("public")
for game in games:
    print(game[2])

#     -- get_game_by_title() - a get query to list a game by game title from Games Table
def get_game_by_title(game_title, privacy_level):
    games_by_title = f"SELECT game_title FROM GAMES where game_tiƒtle = '{game_title}' AND privacy_level = '{privacy_level}';"
    result = search_query(games_by_title)
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
def get_game_details(game):
    game_details = f"SELECT * FROM Games WHERE game_code = SHA2('{game}', 256);"
    result = search_query(game_details)
    game = []
    for record in result:
        game.append(record)
    return game

game = get_game_details(1776)
print(game[0][0])

def get_clues(game_id):
    clues_list = f"SELECT * FROM Clues WHERE game_id = '{ game_id }';"
    result = search_query(clues_list)
    clues = []
    for record in result:
        clues.append(record)
    return clues

clues = get_clues(1)

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

def checkAnswer(clue, input):
    answer_type = clue[2]
    answer = clue[3]
    correct = False
    if answer_type == 'text':
        if answer.lower() == input.lower():
            correct = True
    elif answer_type == 'coordinates':
        correct = True
    return correct

def checkProgress(clues, id):
    total = len(clues)
    completion = (id/total) * 100
    return completion

# completion = checkProgress(clues, 1)
# print(completion)