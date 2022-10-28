-- Python function per page:

-- sign_up.html

    -- create_user() - an insert query into Users Table  (email, user_name, password)
    INSERT INTO Users (email, username, password)
    VALUES ('email', 'username', 'password');

    INSERT INTO Users (email, username, password) 
    VALUES ('guest', 'guest', SHA2('Guest!23', 256));


-- login.html (Users Table)

    -- get_user() - a get query to validate user exists and return user account info 
        -- (associated games created) (email, user_name, password)
    SELECT * FROM Users 
    WHERE user_id = "user_id" AND password = "password";


-- create_game.html

    -- create_game() - an insert query into Games, Clues, and Locations Tables



-- play/search.html

    -- get_game() - a get query to find game by game code from Games Tables

    -- get_game_list() - a get query to list all games from Games Tables

    -- get_game_by_title() - a get query to list a game by game title from Games Table

    -- get_game_by_descr() - a get query to list a game by game description from Games Table

    -- get_most_played_games() - a get query to list the most played games from Games Tables (not sure if we are still doing this)


-- play.html/GAME

    -- get_game_details() - a get query to retrieve all game details based on game code from Games, Clues, and Locations Tables.