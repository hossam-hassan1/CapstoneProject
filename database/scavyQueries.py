# -- Python function per page:

from unittest import result
import mysql.connector

# -- sign_up.html
def create_query(query, success):
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
        print(f"{success}")
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
        VALUES ("{email}", "{username}", "{password}");"""
    success = "User added!"
    create_query(insert, success)
    

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

# get_user('test', 'test')


# create_game.html

#  create_game() - an insert query into Games, Clues, and Locations Tables

def create_game(user_id, game_title, game_description, privacy_level, gps_required, camera_required):
    insert = f"""
    INSERT INTO Games (user_id, game_title, game_description, privacy_level, gps_required, camera_required)
    VALUES ({user_id}, "{game_title}", "{game_description}", "{privacy_level}", "{gps_required}", "{camera_required}");
    """
    success = "Game created!"
    create_query(insert, success)

# create_game(1, "test title", "test description", "public", "true", "false")


# -- play/search.html


#     -- get_game() - a get query to find game by game code from Games Tables
def get_game(game_id):
    games_by_id = f"SELECT game_id FROM Games WHERE game_id = '{game_id}';"
    result = search_query(games_by_id)
    return games_by_id


#     -- get_game_list() - a get query to list all games from Games Tables
def get_game_list(privacy_level):
    list_all_games = f"SELECT game_title FROM Games WHERE privacy_level = '{privacy_level}';"
    result = search_query(list_all_games)
    for game in result:
        print(game)
    return result

# get_game_list('public')

#     -- get_game_by_title() - a get query to list a game by game title from Games Table
def  get_game_by_title(game_title, privacy_level):
    games_by_title = f"SELECT game_title FROM GAMES where game_title = '{game_title}' AND privacy_level = '{privacy_level}';"
    result = search_query(games_by_title)
    for game in result:
        print(game)
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
def get_game_details(game_id):
    get_game_details = f"SELECT * FROM Games WHERE game_id = '{game_id}';"
    get_clue_details = f"SELECT * FROM Clues WHERE game_id = '{game_id}';"
    get_game_location = f"SELECT * FROM Locations WHERE game_id = '{game_id}';"


def get_game_details():
    pass

def get_clue_details():
    pass