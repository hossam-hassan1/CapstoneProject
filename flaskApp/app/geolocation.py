# https://www.geeksforgeeks.org/get-the-city-state-and-country-names-from-latitude-and-longitude-using-python/

# https://nominatim.org/release-docs/develop/api/Reverse/

# https://geopy.readthedocs.io/en/stable/#module-geopy.distance

# https://geopy.readthedocs.io/en/stable/#nominatim

#pip install geopy

from geopy.geocoders import Nominatim

from geopy import distance

# Initialize Nominatim API
geolocator = geolocator = Nominatim(user_agent="scavyApp")

#distance properties from geopy.units, e.g.: km, m, meters, miles and so on.

def displayGameLocation(coordinates):
    # initialize Nominatim API
    location = geolocator.reverse(coordinates)
    address = location.raw['address']
    city = address.get('city', '')
    state = address.get('state', '')
    if city == "":
        county = address.get('county', '')
        return f'{county}, {state}'
    return f'{city}, {state}'

# print()


def searchToCoords(city):
    searchCoords = geolocator.geocode(city)
    searchCoords = (searchCoords.latitude, searchCoords.longitude)
    return searchCoords
# FIND IF POINT WITHIN X OF OTHER POINT
	 
def checkGamesNearby(searchCity, gameLocation, length):
    gameDistance = distance.distance(searchCity, gameLocation).miles
    if gameDistance <= length:
        return True
    return False

# print(checkGamesNearby('hannibal, missouri', 'Hannibal, MO', 20))

# print(checkGamesNearby(mizzouRec, shakespearePizza, 20))
# print(checkGamesNearby(mizzouRec, shakespearePizza, 0.4))
	 
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
            return "On Fire - you are very close to the location!"
        # 70 - 50 <= 20
        elif currentDistance - length <= (length*0.40):
            return "Hotter - you are closer to the location"
        # 80 - 50 <= 30
        elif currentDistance - length <= (length*0.60):
            return 'Hot - you are close to the location'
        # 90 - 50 <= 40
        elif currentDistance - length <= (length*0.80):
            return 'Cold'
        # 95 - 50 = 45 <= 50
        elif currentDistance - length <= length:
            return 'Less Freezing - you less far from the location'
        # 100 - 50 > 50
        elif currentDistance - length > length:
            return 'Freezing - you are far from the location'
        # 100 - 50 <= 50
    except:
        # Some value other than the correct coordinate format
        return "\nSorry, there are difficulties with your check-in. Are you on another planet?"



# mizzouRec = (38.94200875265407, -92.32646834504295)
# ellisLibrary = (38.94438706705483, -92.32644003147516)
# jesseHall = (38.945311945553414, -92.32822378624653)
# stepsJesse = (38.945473, -92.328785)
# columns = (38.946283093377986, -92.32873990291804)
# shakespearePizza = (38.948637004293545, -92.32788402343294)

# recToLibrary = distance.distance(mizzouRec, ellisLibrary).feet
# libraryToJesse = distance.distance(ellisLibrary, jesseHall).feet
# jesseToSteps = distance.distance(jesseHall, stepsJesse).feet
# jesseToColumns = distance.distance(jesseHall, columns).feet
# columnsToShakespeare = distance.distance(columns, shakespearePizza).feet

# print("Rec to Library (in feet): " + str(recToLibrary))
# print("Library to Jesse (in feet): " + str(libraryToJesse))
# print("Jesse to Steps of Jesse (in feet): " + str(jesseToSteps))
# print("Jesse to Columns (in feet): " + str(jesseToColumns))
# print("Columns to Shakespeare (in feet): " + str(columnsToShakespeare))

# print('The columns are in ' + displayGameLocation(columns))
# print('Shakespeares is in ' + displayGameLocation(shakespearePizza))

# checkin45 = (38.94626223288014, -92.32876873666441)
# checkin55 = (38.946147903842935, -92.32879458546917)
# checkin65 = (38.946108599860345, -92.32878587093485)
# checkin75 = (38.946076115102315, -92.32879746998758)
# checkin85 = (38.94606449057896, -92.32879615872548)
# checkin95 = (38.94602884647052, -92.32879519323663)
# stepsJesse = (38.945473, -92.328785)
# error = 'tacos'



# print("Checkin45: " + str(checkClueCoordinate(checkin45, columns, 50)))
# print("Checkin55: " + checkClueCoordinate(checkin55, columns, 50))
# print("Checkin65: " + checkClueCoordinate(checkin65, columns, 50))
# print("Checkin75: " + checkClueCoordinate(checkin75, columns, 50))
# print("Checkin85: " + checkClueCoordinate(checkin85, columns, 50))
# print("Checkin95: " + checkClueCoordinate(checkin95, columns, 50))
# print("Checkin105: " + checkClueCoordinate(stepsJesse, columns, 50))
# print("Error: " + checkClueCoordinate(error, columns, 50))


def stringToCoords(str_coords):
    removeParatheses = str_coords.strip("()")
    removeSpaces = removeParatheses.split(", ")
    list = []
    for i in removeSpaces:
        list.append(float(i))
    coords = tuple(list)
    return coords

print(stringToCoords('(38.94200875265407, -92.32646834504295)'))