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


#     -- create_user() - an insert query into Users Table  (email, user_name, password)
def create_user(email, username, password):
    insert = f"""
        INSERT INTO Users (email, username, password)
        VALUES ("{email}", "{username}", "{password}");"""
    success = "User added!"
    create_query(insert, success)
    
create_user("testemail", "bob", "pass")
# -- login.html (Users Table)

def get_user():
    select = """
    SELECT * FROM Users;
    """
    result = search_query(select)
    

get_user()

#     -- get_user() - a get query to validate user exists and return user account info 
#         -- (associated games created) (email, user_name, password)
#     SELECT * FROM Users 
#     WHERE user_id = "user_id" AND password = "password";


# -- create_game.html

#     -- create_game() - an insert query into Games, Clues, and Locations Tables



# -- play/search.html

#     -- get_game() - a get query to find game by game code from Games Tables

#     -- get_game_list() - a get query to list all games from Games Tables

#     -- get_game_by_title() - a get query to list a game by game title from Games Table

#     -- get_game_by_descr() - a get query to list a game by game description from Games Table

#     -- get_most_played_games() - a get query to list the most played games from Games Tables (not sure if we are still doing this)


# -- play.html/GAME

#     -- get_game_details() - a get query to retrieve all game details based on game code from Games, Clues, and Locations Tables.