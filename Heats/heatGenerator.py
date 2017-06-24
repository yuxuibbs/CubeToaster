import math
import json
import scoresheetsHtml
import pickle
import csv


################################################################################
# Printing Instructions
def printIntro():
    '''
    Prints program name and instructions for the user
    '''
    print("CubeToaster - Heat Generator")
    print("Takes in a JSON file with the competition data and outputs an HTML website with all the score sheets for the competition sorted by heat number")
    print("Type Ctrl-C or Ctrl-Z (whichever one works) to quit the program if something goes wrong.")


def printEnding():
    '''
    Prints instructions for what to do after everything is done
    '''
    print("GROUPS HAVE BEEN GENERATED")
    print("1. Open printableGroups.csv to view group assignments.") 
    print("2. Make sure people with the same first name (or similar names) are not in the same group. You can edit the assignments in the csv file before generating scorecards and still have correct scorecards.")
    print("3. To generate scorecards, run sheetGenerator.py and follow prompts")


################################################################################
# Input validation
def validateInt(prompt):
    '''
    Prompts users until they input an int
    '''
    while True:
        try:
            response = int(input(prompt).strip())
            break
        except:
            continue
    return response


def validateYesNo(prompt):
    '''
    Prompts users until they enter y or n
    '''
    response = ""
    acceptedList = ["y", "yes", "n", "no"]
    while not response in acceptedList:
        response = input(prompt).strip().lower()
    if response == "y" or response == "yes":
        return True
    else:
        return False


def validateInputFile(jsonFile):
    print("Fill out inputData.json (you can leave as many things blank as you want)")
    print("There is a recommended number of groups already listed. You can change it if you want to.")
    print("Everything is based on numGroups (changing numPeople or peoplePerGroup will not change the number of people in each group.)")
   
    while True:
        if validateYesNo("Type y when done. "):
            inputData = getInputInfo()
            print()
            break
    return inputData


################################################################################
# Data Retrieval
def getDataFile():
    '''
    Gets file name from user and reads in the JSON
    '''
    fileName = input('Enter file name (json): ').strip()
    if not fileName.endswith(".json"):
        fileName = fileName + ".json"
    # TODO: get csv or excel data to get accurate competitor ID numbers
    f = open(fileName, "r")
    fileData = json.loads(f.read())
    f.close()
    return fileData


def getStaffList(personList):
    with open("staff.txt", "w") as f:
        with open("competitorList.txt", "w") as comp:
            for person in personList:
                print(person["name"], file=f)
                print(person["name"], file=comp)
    print("Open staff.txt and delete anyone that is NOT on staff")
    while True:
        if validateYesNo("Type y when done. "):
            return readStaffList()


def getCompetitionData(jsonFile):
    """
    Parses JSON into a data structure
    Returns (competitionId, events)
    """
    competitionId = jsonFile["competitionId"]
    persons = {}
    events = {}

    staffList = getStaffList(jsonFile["persons"])

    for person in jsonFile["persons"]:
        # remove unnecessary data (WCA ID, country, gender, and dob)
        del person["wcaId"]
        del person["countryId"]
        del person["gender"]
        del person["dob"]
        # make sure name is in title case
        person["name"] = person["name"].title()
        # initialize heat number
        person["heat"] = 0
        if person["name"] in staffList:
            person["staff"] = 1
        else:
            person["staff"] = 0
        # put person data into a dictionary with id number as key
        persons[person["id"]] = person

    for event in jsonFile["events"]:
        results = []
        # replace id in events part of JSON with the person's data
        for person in event["rounds"][0]["results"]:
            try:
                results.append(persons[person["personId"]].copy())
            except:
                print("POSSIBLE ERROR: Make sure all registered competitors are in competitors.txt")
        results.sort(key=lambda x: (-x["staff"], x["name"].lower()))
        event["rounds"][0]["results"] = results
        events[event["eventId"]] = event

    return (competitionId, events)


def readStaffList():
    staff = []
    with open("staff.txt", "r") as f:
        for line in f:
            staff.append(line.strip())
    return staff


def getInputInfo():
    f = open("inputData.json", "r")
    inputData = json.loads(f.read())
    f.close()
    return inputData

def changeCompetitionName(jsonData):
    compName = input("Input competition name: ")
    jsonData['competitionId'] = compName


################################################################################
# Everything related to making/calculating heats
def calcNumHeats(compData, eventsDict, inputData):
    '''
    Gets number of heats for each event from user
    recommended number of people per heat: ceil(1.5*numStations) to the nearest even number
    '''
    heatsDict = {}
    for event in compData[1]:
        numPeople = len(compData[1][event]["rounds"][0]["results"])
        if event == "444bf" or event == "555bf" or event == "333fm" or event == "333mbf":
            heatsDict[event] = 1
        else:
            heatsDict[event] = inputData[event]["numGroups"]
        if heatsDict[event] == 1:
            print("There will be 1 group for {0} for {1} people".format(eventsDict[event], numPeople))
        else:
            print("There will be {0} groups for {1} for {2} people".format(heatsDict[event], eventsDict[event], numPeople))
    return heatsDict
   

def easyHeats(compData, heatsDict):
    '''
    Goes straight down list of competitors from 1 to numPeopleInHeats
    '''
    ''' TODO: later
    staff = False
    # assumes that number of people on staff is always less than 60% of the number of people in 3x3x3
    if len(staffList) < len(compData[1][event]["rounds"][0]["results"]) * 0.6:
        staff = True
    '''
    for event in heatsDict:
        for i, person in enumerate(compData[1][event]["rounds"][0]["results"]):
            if (heatsDict[event] != 0):
                person["heat"] = (i % heatsDict[event]) + 1

    return compData


def makeCompetitorList(jsonFile):
    '''
    Creates txt file with all of the competitors at the competition
    '''
    # print to file
    with open("competitors.txt", "w") as f:
        for person in jsonFile["persons"]:
            print(person["name"], file=f)


################################################################################
# Create output files
def createInputFile(compData):
    '''
    creates json file for users to edit number of people per heat and cutoffs
    '''
    data = {}
    fastEvents = ["222", "333", "333oh", "skewb", "pyram"]

    numStations = validateInt("How many timing stations will you be using per stage? ")
   
    for event in compData[1]:
        inputData = {}
        numPeople = len(compData[1][event]["rounds"][0]["results"])
       
        if event in fastEvents:
            recommendNumHeats = round(numPeople / (1.7 * numStations))
        else:
            recommendNumHeats = round(numPeople / (1.5 * numStations))
        if recommendNumHeats < 1:
            recommendNumHeats = 1

        inputData["numPeople"] = numPeople
        inputData["numGroups"] = recommendNumHeats
        inputData["cutoff"] = ""
        inputData["timeLimit"] = ""
        inputData["peoplePerGroup"] = numPeople / recommendNumHeats
        # inputData["usePsychSheet?"] = "no"
       
        data[event] = inputData

    with open("inputData.json", "w") as f:
        print(json.dumps(data, indent=4), file=f)


def makePrintableHeatSheet(assignedHeats, jsonFile, heatsDict, eventsDict):
    '''
    Gets all the heats for each competitor and turns it into a printable format
    Makes a list of [name, [list of events with heat numbers]]
        sorted by name (with events sorted by alphabetical order)
    outputs:
        file with everyone's heat numbers on it
        file with everyone's names on it (for use in staff stuff later)
    '''
    # make list of dictionaries with person name and all the events
    competitorHeats = []
    for person in jsonFile["persons"]:
        tempDict = {}
        tempDict["name"] = person["name"]
        for event in assignedHeats[1]:
            for personData in assignedHeats[1][event]["rounds"][0]["results"]:
                if person["name"] == personData["name"]:
                    heatNum = personData["heat"]
                    tempDict[event] = heatNum
        if tempDict not in competitorHeats:
            competitorHeats.append(tempDict)

    # make competitorHeats sortable by event name
    printableHeats = []
    for competitor in competitorHeats:
        tempList = []
        for key, value in competitor.items():
            if key != "name":
                tempTuple = ()
                tempTuple = (key, value)
                tempList.append(tempTuple)
        printableHeats.append([competitor["name"], tempList])

    for person in printableHeats:
        person[1].sort(key=lambda x: x[0])
    printableHeats.sort()

    # sort by first name
    competitorHeats.sort(key=lambda x: x['name'])
    # print heat sheet to csv file
    with open("printableGroups.csv", "w", newline="") as f:
        columnNames = ["name"] + list(eventsDict.keys())
        heatWriter = csv.DictWriter(f, fieldnames=columnNames, delimiter=",")
        heatWriter.writeheader()
        for person in competitorHeats:
            heatWriter.writerow(person)

    # REMOVE WHEN CUBECOMPS TAKES JSON STUFF
    newIDs = {}
    newNum = 1
    for person in printableHeats:
        newIDs[person[0]] = str(newNum)
        newNum += 1
    with open("testCompetitorID.txt", "w") as f:
        for person in printableHeats:
            print(person[0], newIDs[person[0]], file=f)
    return newIDs

################################################################################
# Main
def main():
    printIntro()
    print()

    jsonFile = getDataFile()

    changeCompetitionName(jsonFile)

    compData = getCompetitionData(jsonFile)

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

    # get user input to make heats
    createInputFile(compData)
    print()
    inputData = validateInputFile(jsonFile)
    # figure out how many heats there will be for each event
    heatsDict = calcNumHeats(compData, eventsDict, inputData)
    # assign heats
    assignedHeats = easyHeats(compData, heatsDict)

    # make output files
    # heats
    # CHANGE WHEN CUBECOMPS TAKES JSON STUFF
    newIDs = makePrintableHeatSheet(assignedHeats, jsonFile, heatsDict, eventsDict)
    
    # Save assignedHeats, heatsDict, eventsDict, inputData, newIDs to files for sheetGenerator.py to read. Done with help from http://stackoverflow.com/questions/6568007/how-do-i-save-and-restore-multiple-variables-in-python
    with open('objs.pickle', 'wb') as f:
        pickle.dump([assignedHeats[0], heatsDict, eventsDict, inputData, newIDs], f)
    
    print()
    printEnding()
    # print(json.dumps(assignedHeats, indent=2))

if __name__ == '__main__':
    main()