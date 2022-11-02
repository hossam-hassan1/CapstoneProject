DROP DATABASE scavyDB;

CREATE DATABASE scavyDB;

USE scavyDB;

CREATE TABLE Users (
    user_id int NOT NULL AUTO_INCREMENT,
    email char(255) NOT NULL UNIQUE,
    username char(100) NOT NULL UNIQUE,
    password char(255) NOT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE Games (
    game_id int NOT NULL AUTO_INCREMENT,
    user_id int NOT NULL,
    game_title char(100) NOT NULL,
    game_description text(500) NOT NULL,
    geo_location char(255) DEFAULT NULL,
    privacy_level ENUM('public', 'private') NOT NULL,
    gps_required ENUM('true', 'false') NOT NULL,
    camera_required ENUM('true', 'false') NOT NULL,
    created_on DATE,
    play_count int DEFAULT 0,
    game_code char(255) NOT NULL,
    PRIMARY KEY (game_id)
);

CREATE TABLE Locations (
    location_id int NOT NULL AUTO_INCREMENT,
    game_id int NOT NULL,
    geo_location char(255) NOT NULL,  
        -- need to identify how user checks this location
    PRIMARY KEY (location_id),
    FOREIGN KEY (game_id) REFERENCES Games(game_id)
);

CREATE TABLE Clues (
    clue_id int NOT NULL AUTO_INCREMENT,
    game_id int NOT NULL,
    prompt_text text(1000) NOT NULL,
    prompt_link text (1000),
    prompt_image mediumblob,
    answer_type ENUM('coordinates', 'text') NOT NULL,
    -- error checking to make sure clues are near game location
    answer text(1000) NOT NULL,
    PRIMARY KEY (clue_id),
    FOREIGN KEY (game_id) REFERENCES Games(game_id)
);

-----------------------TEST DATA---------------------------

-- Test User
    INSERT INTO Users (email, username, password)
    VALUES ('test@gmail.com', 'test', SHA2('test', 256));

-- Test Games
    INSERT INTO Games (user_id, game_title, game_description, geo_location, privacy_level, gps_required, camera_required, game_code)
    VALUES 
    (1, "Mizzou Quest", "New to the University of Missouri? Try MizzouQuest to discover some favorite spots on campus.", "Columbia, MO", "public", "true", "false", SHA2('1776', 256)),
    (1, "Hannibal Hunt", "Discover these cool Hannibal Landmarks with this fun scavenger hunt!", "Hannibal, MO", "public", "true", "false", SHA2('1776', 256));

-- Test Clues

    INSERT INTO Clues (game_id, prompt_text, answer_type, answer)
    VALUES 
    -- Mizzou
    (1, 'Your MU Tigers work out here and you can too!\nFind this place.', "coordinates", "'38.94200875265407, -92.32646834504295'"),
    (1, 'Now that you have worked up a sweat, lets work out your brain. \n\nWhere would you go to borrow some books?', "coordinates", '38.945311945553414, -92.32822378624653'),
    (1, 'Facts about this domed building: \n1. Function: Administrative Building.\n2. Adjacent concert auditorium.\n3. Featured on most Mizzou promotions.\nFind this location.', 'coordinates', '38.945311945553414, -92.32822378624653'),
    (1, 'Here you will walk the Tiger Walk through these as a freshman and the Tiger Prowl as a senior. You should be pretty close by... \nFind the location of this MU tradition.', 'coordinates', '38.946655199979766, -92.32879005760252'),
    (1, 'To eat pizza, or not to eat pizza? There really is no question. \nHead to the best pizza place in town.', 'coordinates', '38.948637004293545, -92.32788402343294'),
    -- Hannibal Hunt
    (2, 'Does a boy get a chance to whitewash a fence every day? Enter the last word on the sign located here.','text', 'Done'),
    (2, 'Hannibals oldest, family restaurant has been serving the downtown for four generations. They have an iconic sign spinning mug in their parking lot. What do they serve out of their mug?', 'text', 'Root Beer'),
    (2, '"...Now and then we had a hope that if we lived and were good, God would permit us to be pirates. These ambitions faded out, each in its turn; but the ambition to be a steamboatman always remained." \n- Life on the Mississippi, Mark Twain \nFind Mark Twain as a steamboatman. What does he say is his profession?', 'text', 'Steamboat Pilot'),
    (2, 'Hannibal has over a dozen public murals. Some are over 30 feet tall! One features a woman about to board a train. What color is her dress?', 'text', 'Green'),
    (2, 'Did you know that the light house in Hannibal is strictly decorative? Riverboats do not need it. But when it was installed in 1935 President FDR pushed a button a the White House to light it for the first time. How many steps is it to the lighthouse from Main Street?', 'text', '244');

-- Test Locations
    INSERT INTO Locations (game_id, geo_location)
    VALUES 
    -- Columbia
    (1, "Columbia, MO"),
    -- Hannibal
    (2, "Hannibal, MO");

