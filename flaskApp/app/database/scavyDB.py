
import mysql.connector

dropDB = "DROP DATABASE scavyapp$default;"
createDB = "CREATE DATABASE scavyapp$default;"

useDB = "USE scavyapp$default;"

createUsers = """
CREATE TABLE Users (
    user_id int NOT NULL AUTO_INCREMENT,
    email char(255) NOT NULL UNIQUE,
    username char(100) NOT NULL UNIQUE,
    password char(255) NOT NULL,
    PRIMARY KEY (user_id)
);
"""

createGames = """
CREATE TABLE Games (
    game_id int NOT NULL AUTO_INCREMENT,
    user_id int NOT NULL,
    game_title char(100) NOT NULL UNIQUE,
    game_description text(500) NOT NULL,
    geo_location char(255) DEFAULT "NULL",
    privacy_level ENUM('public', 'private') NOT NULL,
    gps_required ENUM('true', 'false') NOT NULL,
    camera_required ENUM('true', 'false') NOT NULL,
    created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    play_count int DEFAULT 0,
    game_code char(255) UNIQUE NOT NULL,
    published ENUM('true', 'false') DEFAULT 'false',
    FULLTEXT(game_title,game_description),
    PRIMARY KEY (game_id)
);
"""

createLocations = """
CREATE TABLE Locations (
    location_id int NOT NULL AUTO_INCREMENT,
    game_id int NOT NULL,
    geo_location char(255) NOT NULL,
    PRIMARY KEY (location_id),
    FOREIGN KEY (game_id) REFERENCES Games(game_id) ON DELETE CASCADE
);
"""

createClues = """
CREATE TABLE Clues (
    clue_id int NOT NULL AUTO_INCREMENT,
    game_id int NOT NULL,
    clue_order int NOT NULL,
    prompt_text text(1000) NOT NULL,
    prompt_link text (1000),
    prompt_image char(255),
    answer_type ENUM('coordinates', 'text') NOT NULL,
    answer text(1000) NOT NULL,
    PRIMARY KEY (clue_id),
    FOREIGN KEY (game_id) REFERENCES Games(game_id) ON DELETE CASCADE
);
"""

testUser = """INSERT INTO Users (email, username, password)
    VALUES ('test@gmail.com', 'scavyApp', SHA2('scavyApp1!', 256));"""

testGames = """INSERT INTO Games (user_id, game_title, game_description, geo_location, privacy_level, gps_required, camera_required, game_code, published)
    VALUES
    (1, "Mizzou Quest", "New to the University of Missouri? Try MizzouQuest to discover some favorite spots on campus.", "Columbia, MO", "public", "true", "false", '1776', 'false'),
    (1, "Hannibal Hunt", "Discover these cool Hannibal, Missouri Landmarks with this fun scavenger hunt!", "Hannibal, MO", "public", "true", "false", '1942', 'true'),
    (1, "Hannibal Hunt Geolocation", "Discover these cool Hannibal, Missouri Landmarks with this fun scavenger hunt!", "Hannibal, MO", "public", "true", "false", 'Hann1942', 'true'),
    (1, "Private Test", "private", "private", "private", "true", "false", 'private', 'true');
"""

testClues = """INSERT INTO Clues (game_id, clue_order, prompt_text, answer_type, answer)
    VALUES
    -- Mizzou
    (1, 1, 'Your MU Tigers work out here and you can too!\nFind this place.', "coordinates", "38.94200875265407, -92.32646834504295"),
    (1, 2, 'Now that you have worked up a sweat, lets work out your brain. \n\nWhere would you go to borrow some books?', "coordinates", '38.94438706705483, -92.32644003147516'),
    (1, 3, 'Facts about this domed building: \n1. Function: Administrative Building.\n2. Adjacent concert auditorium.\n3. Featured on most Mizzou promotions.\nFind this location.', 'coordinates', '38.945311945553414, -92.32822378624653'),
    (1, 4, 'Here you will walk the Tiger Walk through these as a freshman and the Tiger Prowl as a senior. You should be pretty close by... \nFind the location of this MU tradition.', 'coordinates', '38.946283093377986, -92.32873990291804'),
    (1, 5, 'To eat pizza, or not to eat pizza? There really is no question. \nHead to the best pizza place in town.', 'coordinates', '38.948637004293545, -92.32788402343294'),
    -- Hannibal Hunt
    (2, 1, 'Does a boy get a chance to whitewash a fence every day? Enter the last word on the sign located here.','text', 'Done'),
    (2, 2, 'Hannibals oldest, family restaurant has been serving the downtown for four generations. They have an iconic sign spinning mug in their parking lot. What do they serve out of their mug?', 'text', 'Root Beer'),
    (2, 3, '"...Now and then we had a hope that if we lived and were good, God would permit us to be pirates. These ambitions faded out, each in its turn; but the ambition to be a steamboatman always remained." \n- Life on the Mississippi, Mark Twain \nFind Mark Twain as a steamboatman. What does he say is his profession?', 'text', 'Steamboat Pilot'),
    (2, 4, 'Hannibal has over a dozen public murals. Some are over 30 feet tall! One features a woman about to board a train. What color is her dress?', 'text', 'Green'),
    (2, 5, 'Did you know that the light house in Hannibal is strictly decorative? Riverboats do not need it. But when it was installed in 1935 President FDR pushed a button a the White House to light it for the first time. How many steps is it to the lighthouse from Main Street?', 'text', '244'),
     -- Hannibal Hunt Geolocation
    (3, 1, 'Hannibals oldest, family restaurant has been serving the downtown for four generations. They have an iconic sign spinning mug in their parking lot. What do they serve out of their mug?', 'coordinates', '39.71207977376028, -91.35859090451727'),
    (3, 2, 'Does a boy get a chance to whitewash a fence every day? Enter the last word on the sign located here.', 'coordinates', '39.71195081958449, -91.35780176501078'),
    (3, 3, '"...Now and then we had a hope that if we lived and were good, God would permit us to be pirates. These ambitions faded out, each in its turn; but the ambition to be a steamboatman always remained." \n- Life on the Mississippi, Mark Twain \nFind Mark Twain as a steamboatman. What does he say is his profession?', 'coordinates', '39.71253188272878, -91.35528171488045'),
    (3, 4, 'Hannibal has over a dozen public murals. Some are over 30 feet tall! One features a woman about to board a train. What color is her dress?', 'coordinates', '39.71074090151194, -91.35611319952365'),
    (3, 5, 'Did you know that the light house in Hannibal is strictly decorative? Riverboats do not need it. But when it was installed in 1935 President FDR pushed a button a the White House to light it for the first time. How many steps is it to the lighthouse from Main Street?', 'coordinates', '39.714603033439445, -91.35896606556047'),
    -- Private Test Game
    (4, 1, 'private test','text', 'private');
"""

testLocations = """INSERT INTO Locations (game_id, geo_location)
    VALUES
    -- Columbia
    (1, "Columbia, MO"),
    -- Hannibal
    (2, "Hannibal, MO");"""


def buildDatabase():
#create a connector object
    try:
        mydb = mysql.connector.connect(
            host="scavyapp.mysql.pythonanywhere-services.com",
            user="scavyapp",
            passwd="scavy123!",
        )


        #create database cursor
        mycursor = mydb.cursor()

        #drop database
        mycursor.execute(dropDB)

        #create database
        mycursor.execute(createDB)

        #use database
        mycursor.execute(useDB)

        #create tables
        mycursor.execute(createUsers)

        mycursor.execute(createGames)
        mycursor.execute(createLocations)
        mycursor.execute(createClues)

        # addTestData
        mycursor.execute(testUser)
        mycursor.execute(testGames)
        mycursor.execute(testClues)
        mycursor.execute(testLocations)

        mydb.commit()

        print("ScavyApp Database Created Successfully!")

    except Exception as err:
        print(f"Error Occured: {err}\nExiting program...")
        quit()


buildDatabase()