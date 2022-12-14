# -- Python function per page:
import mysql.connector
import random
import os
from geopy.geocoders import Nominatim
from geopy import distance
from app.geolocation import displayGameLocation, checkGamesNearby, searchToCoords


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
        print(mycursor.rowcount, "record(s) affected after INSERT")
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

def search_one_query(query):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            database="scavyDB",
            user="root",
            passwd="pass"
        )
        mycursor = mydb.cursor()
        mycursor.execute(query)
        query_result = mycursor.fetchone()[0]
        return query_result
    except Exception as err:
        print(f"Error Occured: {err}\nExiting program...")
        quit()

def update_query(query):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            database="scavyDB",
            user="root",
            passwd="pass"
        )
        mycursor = mydb.cursor()
        mycursor.execute(query)
        print(mycursor.rowcount, "record(s) affected after UPDATE")
        mydb.commit()
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
        print("user does not exist")

#     -- get_game_by_title() - a get query to list a game by game title from Games Table
def get_game_by_title(game_title):
    games_by_title = f"SELECT game_id FROM Games where game_title = '{game_title}';"
    try:
        result = search_query(games_by_title)   
        # print(result)
        if result[0] == []:
            return result
    except:
        return result
    return result[0][0]


def find_play_count(game_id):
    select_game = f"""
        SELECT play_count FROM Games WHERE game_id = "{game_id}";
        """
    result = search_one_query(select_game)
    print("find play count result: ", result)
    print("find play count result TYPE: ", (type(result)))
    return result

# logs how many times a game is played add "{game_id}"
def log_play_count(total_count, game_id):
    update = f"""
        UPDATE Games SET play_count = "{total_count}" WHERE game_id = "{game_id}";
        """
    result = update_query(update)
    print("log play count result: ", result)
    return result


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
        error = False
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

def stringToCoords(str_coords):
    removeParatheses = str_coords.strip("()")
    removeSpaces = removeParatheses.split(", ")
    list = []
    for i in removeSpaces:
        list.append(float(i))
    coords = tuple(list)
    return coords

# print(stringToCoords('(38.94200875265407, -92.32646834504295)'))

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

#  create_game() - an insert query into Games, Clues, and Locations Tables
def create_game(user_id, game_title, game_description, privacy_level, gps_required, camera_required, geo_location):
    game_id = get_game_by_title(game_title)
    # print(f'Game ID: {game_id}')
    game_code = generate_game_code(game_title)
    # add cords into insert and values    188,192,193
    if geo_location == 'Virtual':
        location = geo_location
    else:
        coordinates = stringToCoords(geo_location)
        location = displayGameLocation(coordinates)
    insert = f"""
    INSERT INTO Games (user_id, game_title, game_description, privacy_level, gps_required, camera_required, game_code, geo_location)
    VALUES ({user_id}, "{game_title}", "{game_description}", "{privacy_level}", "{gps_required}", "{camera_required}", "{game_code}", "{location}");
    """
    # try:
    try:
        game_id = create_query(insert)
        created = True
        message = f"Game: '{game_title}' has been created!"
    except:
        created = False
        # print(game_id)
        if game_id != []:
            message = f"{game_title} already exists. Game titles are unique in ScavyApp and give each game their own link. Please try creating a game with a different title."
        else:
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

def delete_game(game_id):
    delete_game = f"""
        DELETE FROM Games WHERE game_id = {game_id};
    """
    # try:
    try:
        game = create_query(delete_game)
        print(game)
        return 'Game has been deleted.'
    except:
        return 'Game could not be deleted.'

# # most played
# most_played = '''SELECT * 
#                 FROM Games 
#                 WHERE privacy_level = "public" AND published = "true"
#                 ORDER BY play_count desc LIMIT 10;'''

# keyword
keyword = '''SELECT * FROM Games 
            WHERE privacy_level = "public" AND published = "true" AND  MATCH (game_title, game_description)
            AGAINST('Missouri' IN NATURAL LANGUAGE MODE);'''

# location
# location = 'SELECT * FROM Games WHERE geo_location = geo_location;'

# gps_requirement
gps_required = 'SELECT * FROM Games WHERE gps_required = "true" AND privacy_level = "public" AND published = "true";'

# camera requirement
camera_required = 'SELECT * FROM Games WHERE camera_required = "true" AND privacy_level = "public" AND published = "true";'


#     -- get_game_list() - a get query to list all games from Games Tables
def get_game_list(filter, input):
    additional_query = ''
    extra_order = 'ORDER BY user_id=1 desc;'
    if filter == 'all-games':
        additional_query = ''
    elif filter == 'most-played':
        additional_query = ' AND play_count >= 1 ORDER BY play_count desc LIMIT 10'
        extra_order = ''
    elif filter == 'gps-required':
        additional_query = 'AND gps_required = "true"'
    elif filter == 'camera-required':
        additional_query = 'AND camera_required = "true"'
    elif filter == 'location':
        if input.lower() == 'virtual': 
            additional_query = 'AND geo_location = "Virtual"'
    elif filter == 'keyword':
        additional_query = f'''AND MATCH (game_title, game_description) 
                        AGAINST('{input}' IN NATURAL LANGUAGE MODE)'''
    else:
        pass
    list_all_games = f'''SELECT * FROM Games 
                        WHERE privacy_level = 'public' AND published = 'true'
                        {additional_query} {extra_order};'''
    result = search_query(list_all_games)
    games = []
    
    for record in result:
        # items = []
        # for item in record:
        #     items.append(item)
        games.append(record)
    if filter == 'location' and input == '':
        pass
    elif filter == 'location' and input.lower() != 'virtual':
        location_search = []
        # print(input)
        try:
            input = searchToCoords(input)
            # print(input)
            for game in games:
                geo_location = searchToCoords(game[4])
                try:
                    check = checkGamesNearby(input, geo_location, 25)
                    # print(f'Geolocation: {geo_location} {check}')
                    if check == True:
                        location_search.append(game)
                except:
                    pass
                    # print("error")
            return location_search
        except:
            # print('Not valid location')
            pass
    return games


# games = get_game_list("public")
# for game in games:
#     print(game[2])

def get_game_by_id(game_id):
    game = f"SELECT * FROM Games where game_id = '{game_id}';"
    result = search_query(game)
    return result[0]

#     -- get_game_by_descr() - a get query to list a game by game description from Games Table
def get_game_location(game_description, privacy_level):
    games_by_description = f"SELECT game_title FROM Games where game_description = '{game_description}' AND privacy_level = '{privacy_level}';"
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
    game_details = f"SELECT * FROM Games WHERE game_code = '{game}';"
    code_message = ""
    exists = False
    try:
        result = search_query(game_details)
        print(len(result))
        if len(result) == 1:
            exists = True
            print(exists)
            game = []
            for record in result:
                game.append(record)
            game_id = game[0][0]
            print(game_id)
            name = game[0][2]
            print(name)
            name = name.replace(" ", "_")
        else:
            exists = False
            name = False
            game_id = False
            code_message = "Game code does not exist."
    except:
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

def get_clues(game_id):
    clues_list = f"SELECT * FROM Clues WHERE game_id = '{ game_id }' ORDER BY clue_order;"
    result = search_query(clues_list)
    clues = []
    for record in result:
        clues.append(record)
    return clues

def check_privacy(game_id):
    privacy_query = f"SELECT privacy_level FROM Games WHERE game_id = '{game_id}';"
    result = search_query(privacy_query)
    privacy = ''
    for record in result:
        for level in record: 
            privacy = level
    return privacy


def getClue(clues, id, game):
    total = len(clues)
    if id < total:
        clue = clues[id] 
        clue_id = id + 1
        prompt = clue[3]
        prompt_link = clue[4]
        prompt_image = clue[5]
        answer_type = clue[6]
        answer = clue[7]
    else:
        clue_id = -1
        prompt = f"Congrats! You have completed {game}."
        prompt_link = ""
        prompt_image = ''
        answer_type = ""
        answer = ""
    return clue_id, prompt, prompt_link, prompt_image, answer_type, answer, 


def checkClueCoordinate(checkin, answer, length):
    try:
        currentDistance = distance.distance(checkin, answer).feet
        # print("\n")
        # print(currentDistance)
        # 50 - 50 <= 50
        if currentDistance <= length:
            return True
        # 60 - 50 <= 10
        elif currentDistance - length <= (length*0.20):
            return "On Fire<br>\U0001F525 \U0001F525 \U0001F525"
        # 70 - 50 <= 20
        elif currentDistance - length <= (length*0.40):
            return "Hotter<br>\U0001F525 \U0001F525"
        # 80 - 50 <= 30
        elif currentDistance - length <= (length*0.60):
            return 'Hot<br>\U0001F525'
        # 90 - 50 <= 40
        elif currentDistance - length <= (length*0.80):
            return 'Cold<br>\U0001F976'
        # 95 - 50 = 45 <= 50
        elif currentDistance - length <= length:
            return 'Less Freezing<br>\U0001F976 \U0001F976'
        # 100 - 50 > 50
        elif currentDistance - length > length:
            return 'Freezing<br>\U0001F976 \U0001F976 \U0001F976'
        # 100 - 50 <= 50
    except:
        # Some value other than the correct coordinate format
        return "\nSorry, there are difficulties with your check-in. Please try again."

def checkAnswer(clue, input):
    answer_type = clue[4]
    print(answer_type)
    answer = clue[5]
    if answer_type == 'text':
        if answer.lower() == input.lower():
            return True
        else:
            return False
    elif answer_type == 'coordinates':
        answer = stringToCoords(answer)
        # answer = answer.split(", ")
        # answer = (float(answer[0]), float(answer[1]))
        # print(answer)
        # change 50 to large number for success
        checkin = checkClueCoordinate(input, answer, 50)
        if checkin == True:
            return True
        else:
            return checkin
    else:
        return "Error with Check Answer"

def checkProgress(clues, id):
    total = len(clues)
    try:
        completion = (id/total) * 100
        return completion
    except:
        print("checkProgress completion failed in scavyQueries.py")
    


def check_form_boxes(privacy_level, camera_required, gps_required, geolocation):
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
    if geolocation == 'Virtual':
        physical_radio = ''
        virtual_radio = 'checked'
    else: 
        physical_radio = 'checked'
        virtual_radio = ''
    return public_radio, private_radio, camera_box, gps_box, physical_radio, virtual_radio



def load_edit_form(game_id):
    game = get_game_by_id(game_id)
    # print(game)
    # print(game)
    game_title = game[2]
    game_description = game[3]
    geo_location = game[4]
    boxes = check_form_boxes(game[5], game[7], game[6], game[4])
    public_radio = boxes[0]
    private_radio = boxes[1]
    camera_box = boxes[2]
    gps_box = boxes[3]
    physical_radio = boxes[4]
    virtual_radio = boxes[5]
    return game_title, game_description, public_radio, private_radio, gps_box, camera_box, physical_radio, virtual_radio, geo_location

# print(load_edit_form(1))


def save_game_form(game_id, user_id, request, mode):
    message = ''

    game_title = request.form["game_title"]
    
    game_description = request.form["game_description"]
    privacy_level = request.form["privacy_level"]
    geo_location = request.form["coordinates"]
    try:
        camera_required = request.form["camera_required"]
    except:
        camera_required = 'false'
    try:
        gps_required = request.form["gps_required"]
    except:
        gps_required = 'false'
    virtual = request.form["location"]
    print(virtual)
    if virtual == 'Virtual':
        geo_location = "Virtual"
    boxes = check_form_boxes(privacy_level, camera_required, gps_required, geo_location)
    public_radio = boxes[0]
    private_radio = boxes[1]
    camera_box = boxes[2]
    gps_box = boxes[3]
    if mode == 'create':
        if game_title != '' and game_description != '' and geo_location != '':
            game = create_game(user_id, game_title, game_description, privacy_level, gps_required, camera_required, geo_location)
            print(game)
            game_id = game[2]
            message = game[1]
            if game[0] == False:
                return game[0], message
        else:
            message = 'Please fill out missing form fields. '
            if geo_location == '':
                message += 'Please enter coordinates for a geolocation game.'
            return False, message
    # if mode == 'save':
    #     game = get_game_by_id(game_id)
    #     if game_title == '':
    #         game_title = game[2]
    #     if game_description == '':
    #         game_description = game[3]
    #     message = edit_game(game_id, game_title, game_description, privacy_level, gps_required, camera_required)
    return game_title, game_description, public_radio, private_radio, gps_box, camera_box, message, game_id, geo_location

def add_clue_order(game_id):
    clues = get_clues(game_id)
    clue_order = 0
    try:
        last_clue_order = clues[-1][2]
        clue_order = last_clue_order + 1
    except IndexError:
        clue_order = 1
    return clue_order

def edit_clue_order(clue_id, clue_order):
    update = f"""
        UPDATE Clues
        SET clue_order={clue_order}
        WHERE clue_id = {clue_id};
    """
    message = ''
    # try:
    try:
        clue_id = create_query(update)
        message = "Clue order has been updated!"
    except:
        message = 'Game could not be updated.'
    return message

def get_clue(clue_id):
    query = f"""
        SELECT *
        FROM Clues
        WHERE clue_id = {clue_id};
    """
    result = search_query(query)
    clue = result
    return clue[0]


def checkCoordinateAnswerDistance(answer, game_id):
    game = get_game_by_id(game_id)
    game_location = game[4]
    game_location = searchToCoords(game_location)
    answer = stringToCoords(answer)
    check = checkGamesNearby(answer, game_location, 50)
    if check == False:
        return False, 'Wow! This clue is 50 miles away from the rest of your game. Try picking a coordinate closer to the base of your game.'
    return True

def add_clue(game_id, prompt_text, prompt_link, answer_type, answer):
    if answer_type == 'coordinates':
        checkDistance = checkCoordinateAnswerDistance(answer, game_id)
        print(checkDistance)
        if checkDistance != True:
            return checkDistance
    clue_order = add_clue_order(game_id)
    insert = f"""
    INSERT INTO Clues (game_id, clue_order, prompt_text, prompt_link, answer_type, answer)
    VALUES ({game_id}, {clue_order}, '{prompt_text}', '{prompt_link}', '{answer_type}', '{answer}');
    """
    message = ''
    created = False
    clue_id = 0
    try:
        clue_id = create_query(insert)
        created = True
        message = f"Clue#: '{clue_order}' has been created!"
    except:
        message = 'Clue could not be created.'
    return created, message, clue_id

def edit_prompt_image(clue_id, filename):
    update = f"""
        UPDATE Clues
        SET prompt_image='{filename}' 
        WHERE clue_id = {clue_id};
    """
    message = ''
    # try:
    try:
        clue_id = create_query(update)
        message = "Clue has been updated!"
    except:
        message = 'Clue could not be updated.'
    return message

def delete_clue(clue_id, game_id):
    delete_clue = f"""
        DELETE FROM Clues WHERE clue_id = {clue_id};
    """
    delete_order = get_clue(clue_id)[2]
    # try:
    try:
        create_query(delete_clue)
    except:
        return 'Clue could not be deleted.'
    clues = get_clues(game_id)
    for clue in clues:
        clue_order = clue[2]
        if clue[2] > delete_order:
            clue_order = clue[2] - 1
            edit_clue_order(clue[0], clue_order)

def move_clue(clue_id, game_id, direction):
    current_clue_order = get_clue(clue_id)[2]
    clues = get_clues(game_id)
    for clue in clues:
        if direction == 'up':
            clue_order = clue[2]+1
            change_order = current_clue_order-1
        elif direction == 'down':
            clue_order = clue[2]-1
            change_order = current_clue_order+1
        if current_clue_order == clue_order:
            edit_clue_order(clue[0], clue_order)
            edit_clue_order(clue_id, change_order)
            break


# def edit_clue(clue_id, prompt_text, prompt_link, answer_type, answer):
#     update = f"""
#         UPDATE Clues
#         SET prompt_text='{prompt_text}', prompt_link='{prompt_link}', answer_type='{answer_type}', answer='{answer}' 
#         WHERE clue_id = {clue_id};
#     """
#     message = ''
#     # try:
#     try:
#         clue_id = create_query(update)
#         message = "Clue has been updated!"
#     except:
#         message = 'Clue could not be updated.'
#     return message

UPLOAD_FOLDER = '/Users/kennabogue/Documents/MIZZOU/22_FALL/INFOTC_4970_Capstone/CapstoneProject/flaskApp/app/static/prompt_image_uploads'
def delete_user_images(user_id):
    select_images = f'''
                SELECT Clues.prompt_image
                FROM Clues, Games
                WHERE Games.game_id = Clues.game_id AND Games.user_id = {user_id} AND Clues.prompt_image IS NOT NULL;
                '''
    result = search_query(select_images)
    files = []
    for file in result:
        files.append(file[0])
    for file in files:
        filepath = f'{UPLOAD_FOLDER}/{file}'
        if os.path.exists(filepath):
            os.remove(filepath)
        else:
            print("The file does not exist")

def delete_account(user_id):
    delete_account = f"""
        DELETE FROM Users WHERE user_id = {user_id};
    """
    delete_games = f"""
        DELETE FROM Games WHERE user_id = {user_id};
    """
    # try:
    try:
        delete_user_images(user_id)
        create_query(delete_games)
        create_query(delete_account)
    except:
        return 'Account could not be deleted.'

def is_game_published(game_id):
    published = f"SELECT published FROM Games where game_id = '{game_id}';"
    result = search_query(published)
    return result[0][0]

def change_publish(game_id):
    publish = is_game_published(game_id)
    if publish == 'false':
        publish = 'true'
    else:
        publish = 'false'
    update = f"""
        UPDATE Games
        SET published='{publish}' 
        WHERE game_id = {game_id};
    """
    message = ''
    # try:
    try:
        publish = create_query(update)
        if publish == 'true':
            message = "Game has been published!"
        else:
            message = "Game has been unpublished!"
    except:
        message = 'Publish status could not be changed.'
    return message


columns = (38.946283093377986, -92.32873990291804)
checkin45 = (38.94626223288014, -92.32876873666441)
checkin55 = (38.946147903842935, -92.32879458546917)
checkin65 = (38.946108599860345, -92.32878587093485)
checkin75 = (38.946076115102315, -92.32879746998758)
checkin85 = (38.94606449057896, -92.32879615872548)
checkin95 = (38.94602884647052, -92.32879519323663)
stepsJesse = (38.945473, -92.328785)




# clue = get_clue(4)
# answer = clue[7]
# print(answer)
# answer = answer.split(", ")
# answer = (float(answer[0]), float(answer[1]))
# print(answer)
# print(columns)
# verify = checkClueCoordinate(columns, columns, 50)

# clue = [0, 0, 0, 0, 'coordinates',clue[7]]
# answerCheck = checkAnswer(clue, checkin55)

# print(answerCheck)

