import rsa

# HASH PASSWORDS
# -------------------------

do = True
while(do == True):
    help = hash(input())
    hello = hash(input())
    if help == hello:
        print("Hashes Match!")
        do = False
    else:
        print("Try Again.")
    
# ENCRYPT LOCATION
# -------------------------

coordinate = "38.94200875265407, -92.32646834504295"

def separateCoordinates(coordinate):
    longitude = 0
    latitude = 0
    coordinates = x = coordinate.split(", ")
    if len(coordinates) == 2:
        longitude = (coordinates[0])
        latitude = (coordinates[1])
    return latitude, longitude

# this is the string that we will be encrypting
latitude = separateCoordinates(coordinate)[0]
longitude = separateCoordinates(coordinate)[1]
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
    

    
