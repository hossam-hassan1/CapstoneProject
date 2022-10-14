
import mysql.connector
 
createDB = "CREATE DATABASE scavyDB;"

createUsers = """CREATE TABLE Users (
    user_id int NOT NULL AUTO_INCREMENT,
    email char(255) NOT NULL UNIQUE,
    username char(100) NOT NULL UNIQUE,
    password char(20) NOT NULL,
    PRIMARY KEY (user_id)
);
"""

createGames = """CREATE TABLE Games (
    game_id int NOT NULL AUTO_INCREMENT,
    user_id int NOT NULL,
    game_title char(100) NOT NULL,
    game_description char(500) NOT NULL,
    privacy_level tinyint(1) NOT NULL,
    gps_required tinyint(1) NOT NULL,
    camera_required tinyint(1) NOT NULL,
    created_on date DEFAULT GETDATE(),
    PRIMARY KEY (game_id)
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
"""

createLocations = """ CREATE TABLE Locations (
    location_id int NOT NULL AUTO_INCREMENT,
    game_id int NOT NULL,
    geo_location NOT NULL,
    PRIMARY KEY (location_id)
    FOREIGN KEY (game_id) REFERENCES Games(game_id)
);
"""

createClues = """CREATE TABLE Clues (
    clue_id int NOT NULL AUTO_INCREMENT,
    game_id int NOT NULL,
    prompt_text char(1000) NOT NULL,
    answer_type int NOT NULL,
    answer char(1000) NOT NULL,
    PRIMARY KEY (clue_id)
    FOREIGN KEY (game_id) REFERENCES Games(game_id)
)"""

def buildDatabase():
#create a connector object
    try:
        mydb = mysql.connector.connect(
            host="mysql-container",
            user="root",
            passwd="root",
        )
    except Exception as err:
        print(f"Error Occured: {err}\nExiting program...")
        quit()

    #create database cursor
    mycursor = mydb.cursor()

    #execute create statements
    mycursor.execute(createDB)
    mycursor.execute(createUsers)
    mycursor.execute(createLocations)
    mycursor.execute(createClues)

buildDatabase()