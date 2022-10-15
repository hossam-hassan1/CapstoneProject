CREATE DATABASE scavyDB;

USE scavyDB;

CREATE TABLE Users (
    user_id int NOT NULL AUTO_INCREMENT,
    email char(255) NOT NULL UNIQUE,
    username char(100) NOT NULL UNIQUE,
    password char(20) NOT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE Games (
    game_id int NOT NULL AUTO_INCREMENT,
    user_id int NOT NULL,
    game_title char(100) NOT NULL,
    game_description text(500) NOT NULL,
    privacy_level ENUM('public', 'private') NOT NULL,
    gps_required ENUM('true', 'false') NOT NULL,
    camera_required ENUM('true', 'false') NOT NULL,
    created_on DATE,
    PRIMARY KEY (game_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Locations (
    location_id int NOT NULL AUTO_INCREMENT,
    game_id int NOT NULL,
    geo_location char(255) NOT NULL,
    PRIMARY KEY (location_id),
    FOREIGN KEY (game_id) REFERENCES Games(game_id)
);

CREATE TABLE Clues (
    clue_id int NOT NULL AUTO_INCREMENT,
    game_id int NOT NULL,
    prompt_text text(1000) NOT NULL,
    answer_type int NOT NULL,
    answer text(1000) NOT NULL,
    PRIMARY KEY (clue_id),
    FOREIGN KEY (game_id) REFERENCES Games(game_id)
);

