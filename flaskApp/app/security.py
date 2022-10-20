import rsa

# HASH PASSWORDS
# -------------------------

# do = True
# while(do == True):
#     help = hash(input())
#     hello = hash(input())
#     if help == hello:
#         print("Hashes Match!")
#         do = False
#     else:
#         print("Try Again.")
    
# ENCRYPT LOCATION
# -------------------------

# this is the string that we will be encrypting
coordinate = "38.94200875265407, -92.32646834504295"
publicKey, privateKey = rsa.newkeys(512)

def separateCoordinates(coordinate):
    longitude = 0
    latitude = 0
    coordinates = x = coordinate.split(", ")
    if len(coordinates) == 2:
        latitude = (coordinates[0])
        longitude = (coordinates[1])
    return latitude, longitude

latitude, longitude = separateCoordinates(coordinate)
print(latitude)
print(longitude)


# reference: https://www.geeksforgeeks.org/how-to-encrypt-and-decrypt-strings-in-python/
def encryptData(data):
    #generate keys
    #encode message
    encMessage = rsa.encrypt(data.encode(), publicKey)
    decMessage = rsa.decrypt(encMessage, privateKey).decode()
    print("encrypted string: ", encMessage)
    print("decrypted string: ", decMessage)
    return encMessage

encryptData(latitude)
print(latitude)
    
 
def validatePassword(password):
    upper = False
    lower = False
    number = False
    special = False
    length = False
    check = False
    error = []
    if len(password) > 7:
        length = True
        error.append("Password length is not 8 or more characters.")
    for letter in password:
        if letter.isupper() == True:
            upper = True
        elif letter.islower() == True:
            lower = True
        elif letter in ["0","1","2","3","4","5","6","7","8","9"]:
            number = True
        elif letter in ["!", "$", "#", "@", "%", "&"]:
            special = True
    if upper == lower == number == length == special == True:
        check = True
    print(f"""special, /{special}.  
    upper, /{upper}. 
    lower, /{lower}. 
    length, /{length}. 
    number, /{number}. 
    """)
    return check

print(validatePassword("Passw0rdf"))

# print(validatePassword("passwor"))




