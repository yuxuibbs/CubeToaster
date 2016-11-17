import json
import math
from urllib.request import urlopen
from bs4 import BeautifulSoup


def printMenu():
    '''
    Prints program name and instructions for the user
    '''
    print("CubeToaster")
    print("Type Ctrl-C or Ctrl-Z (whichever one works) to quit the program.")
    print()



def getDataFile():
    '''
    Gets file name from user and gets JSON
    '''
    # fileName = input('Enter file name (json):').strip()
    fileName = "Michigan 2016.json"
    f = open(fileName, "r")
    fileData = json.loads(f.read())
    f.close()
    return fileData
'''
    while True:
        try:
            # need authentication to access the page
            url = (input('Enter url of competition website: ')).strip()
            index = url.find('admin')
            jsonURL = url[:index] + 'admin/json.php'
            print(jsonURL)
            data = json.load(open(jsonURL))
            print(data)
            break
            # url = 'https://www.cubingusa.com/Michigan2016/admin/json.php'
        except:
            continue
'''


def getCompetitionData(jsonFile):
    """
    Parses JSON into a data structure
    Returns (competitionId, events)
    """
    competitionId = jsonFile["competitionId"]
    persons = {}
    events = {}

    for person in jsonFile["persons"]:
        # remove dob and replace with initial heat number
        person['heat'] = person.pop('dob')
        person['heat'] = 0
        persons[person["id"]] = person

    for event in jsonFile["events"]:
        results = []
        for person in event["rounds"][0]["results"]:
            results.append(persons[person['personId']])
        results.sort(key=lambda x: x['name'].lower())
        event['rounds'][0]['results'] = results
        events[event['eventId']] = event

    return (competitionId, events)


def getPsychSheet(competitionName, eventsList):
    '''
    Gets the psych sheet data from Stachu's website
    Returns (willMakeCutoff, willNotMakeCutoff)
    '''
    stachuPsychSheet = "http://psychsheets.azurewebsites.net/"
    baseURL = stachuPsychSheet + "/" + competitionName + "/"
    for event in eventsList:
        url = baseURL + event
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "html.parser")
        print(url)

def heatsInEvents(compData):
    '''
    Gets number of heats for each event from user
    '''
    eventsDict = {"222"   : "2x2 Cube",
                  "333"   : "Rubik's Cube",
                  "333oh" : "Rubik's Cube: One-Handed",
                  "333bf" : "Rubik's Cube: Blindfolded",
                  "333fm" : "Rubik's Cube: Fewest moves",
                  "333ft" : "Rubik's Cube: With feet",
                  "333mbf": "Rubik's Cube: Multiple Blindfolded",
                  "444"   : "4x4 Cube",
                  "444bf" : "4x4 Cube: Blindfolded",
                  "555"   : "5x5 Cube",
                  "555bf" : "5x5 Cube: Blindfolded",
                  "666"   : "6x6 Cube",
                  "777"   : "7x7 Cube",
                  "clock" : "Rubik's Clock",
                  "minx"  : "Megaminx",
                  "pyram" : "Pyraminx",
                  "skewb" : "Skewb",
                  "sq1"   : "Square-1"}
    heatsDict = {}
    for event in compData[1]:
        userSure = False
        while not userSure:
            try:
                numPeople = len(compData[1][event]["rounds"][0]["results"])
                numPerHeat = int(input("You have {0} competitors in {1}. How many competitors do you want in each heat? ".format(numPeople, eventsDict[event])).strip())
                confirmed = input("Are you sure you want {0} heats for {1} people in {2}? (Y/N) ".format(numPerHeat, numPeople, eventsDict[event])).strip().lower()
                if confirmed == 'y' and numPerHeat < numPeople and numPerHeat > 0:
                    userSure = True
                    numHeats = math.floor(numPeople/numPerHeat)
                    print("There will be {0} heats in {1}".format(numHeats, eventsDict[event]))
                    heatsDict[event] = numHeats
                else:
                    print("Invalid input. Try again.")
                    continue
            except:
                continue
    return heatsDict


def easyHeats(compData, heatsDict):
    '''
    Goes straight down list of competitors from 1 to numPeopleInHeats
    '''


def main():
    printMenu()

    jsonFile = getDataFile()

    compData = getCompetitionData(jsonFile)
    # print(json.dumps(dataList[1], indent=2))
    # (willMakeCutoff, willNotMakeCutoff) = getPsychSheet(dataList[0], events)
    heatsDict = heatsInEvents(compData)
    print(heatsDict)




if __name__ == '__main__':
    main()