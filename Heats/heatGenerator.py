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
    # fileName = "Michigan 2016.json"
    fileName = "fake.json"
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
        # make dictionary of 
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
    Returns [willMakeCutoff, willNotMakeCutoff]
    '''
    stachuPsychSheet = "http://psychsheets.azurewebsites.net/"
    baseURL = stachuPsychSheet + "/" + competitionName + "/"
    for event in eventsList:
        url = baseURL + event
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "html.parser")
        print(url)

def heatsInEvents(compData, eventsDict):
    '''
    Gets number of heats for each event from user
    '''
    sameNumPerHeat = ''
    while not (sameNumPerHeat == 'y' or sameNumPerHeat == 'n'):
        sameNumPerHeat = input("Same number of people for all events other than 4BLD, 5BLD, multi BLD, and FMC? (y/n) ").strip().lower()

    if sameNumPerHeat == 'y':
        while True:
            try:
                numPerHeat = int(input("How many competitors do you want in each heat? ").strip())
                break
            except:
                continue
        automaticHeats = True
    else:
        automaticHeats = False


    heatsDict = {}
    for event in compData[1]:
        # add if thing to only do events that need special number of people per heat
        numPeople = len(compData[1][event]["rounds"][0]["results"])
        if automaticHeats:
            numHeats = math.floor(numPeople / numPerHeat)
            print("There will be {0} heats in {1}".format(numHeats, eventsDict[event]))
            heatsDict[event] = numHeats
        else:
            userSure = False
            while not userSure:
                try:
                    numPerHeat = int(input("You have {0} competitors in {1}. How many competitors do you want in each heat? ".format(numPeople, eventsDict[event])).strip())
                    confirmed = input("Are you sure you want {0} heats for {1} people in {2}? (Y/N) ".format(numPerHeat, numPeople, eventsDict[event])).strip().lower()
                    if confirmed == 'y' and numPerHeat < numPeople and numPerHeat > 0:
                        userSure = True
                        numHeats = math.floor(numPeople / numPerHeat)
                        print("There will be {0} heats in {1}".format(numHeats, eventsDict[event]))
                        heatsDict[event] = numHeats
                    else:
                        print("Invalid input. Try again.")
                        continue
                except:
                    continue
    return heatsDict

def customHeats(compData):
    '''
    Gets number of heats for each event from user
    '''


def easyHeats(compData, heatsDict):
    '''
    Goes straight down list of competitors from 1 to numPeopleInHeats
    '''
    # print(json.dumps(compData, indent=2))
    for event in heatsDict:
        test = []
        test1 = {}
        print("heatsDict[event]", heatsDict[event])
        for person in compData[1][event]["rounds"][0]["results"]:
            person["heat"] = (compData[1][event]["rounds"][0]["results"].index(person) % heatsDict[event]) + 1
            print(person)
            # print("heat number:", (compData[1][event]["rounds"][0]["results"].index(person) % heatsDict[event]) + 1)
            test.append((compData[1][event]["rounds"][0]["results"].index(person) % heatsDict[event]) + 1)
        
        for num in test:
            if num not in test1:
                test1[num] = 0
            test1[num] += 1
        print(test1)

    return compData


def main():
    printMenu()

    jsonFile = getDataFile()

    compData = getCompetitionData(jsonFile)
    # print(json.dumps(dataList[1], indent=2))
    # (willMakeCutoff, willNotMakeCutoff) = getPsychSheet(dataList[0], events)
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
    heatsDict = heatsInEvents(compData, eventsDict)

    finishedHeats = easyHeats(compData, heatsDict)
    print(heatsDict)
    print(json.dumps(finishedHeats, indent=2))




if __name__ == '__main__':
    main()