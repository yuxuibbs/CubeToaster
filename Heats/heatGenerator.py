import json
import math
import scoresheetsHtml


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
    while not (response == 'y' or response == 'n'):
        response = input(prompt).strip().lower()
    return response


def printMenu():
    '''
    Prints program name and instructions for the user
    '''
    print("CubeToaster")
    print("Takes in a JSON file with the competition data and outputs an HTML website with all the scoresheets for the competition sorted by heat number")
    print("Type Ctrl-C or Ctrl-Z (whichever one works) to quit the program if something goes wrong.")
    print()



def getDataFile():
    '''
    Gets file name from user and reads in the JSON
    '''
    # fileName = input('Enter file name (json):').strip()
    # fileName = "Michigan 2016.json"
    # TODO: get csv data to get accurate competitor ID numbers
    fileName = "fake gamma.json"
    f = open(fileName, "r")
    fileData = json.loads(f.read())
    f.close()
    return fileData


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
        # put person data into a dictionary with id number as key
        persons[person["id"]] = person

    for event in jsonFile["events"]:
        results = []
        # replace id in events part of JSON with the person's data
        for person in event["rounds"][0]["results"]:
            results.append(persons[person['personId']].copy())
        results.sort(key=lambda x: x['name'].lower())
        event['rounds'][0]['results'] = results
        events[event['eventId']] = event

    return (competitionId, events)


def createInputFile(heatsDict):
    '''
    creates json file for users to edit number of people per heat and cutoffs
    '''
    # Need to figure out how the competition organizers want to input data



def calcNumHeats(compData, eventsDict):
    '''
    Gets number of heats for each event from user
    recommended number of people per heat: ceil(1.5*numStations) to the nearest even number
    '''
    sameNumPerHeat = validateYesNo("Same number of people for all events other than 4BLD, 5BLD, multi BLD, and FMC? (y/n) ")
    
    if sameNumPerHeat == 'y':
        numPerHeat = validateInt("How many competitors do you want in each heat? ")
        automaticHeats = True
    else:
        automaticHeats = False

    print()

    heatsDict = {}
    for event in compData[1]:
        numPeople = len(compData[1][event]["rounds"][0]["results"])
        if automaticHeats:
            if event == "444bf" or event == "555bf" or event == "333fm" or event == "333mbf":
                # preparing to have a JSON that gets all necessary user input information
                # heatsDict[event]["numPeoplePerHeat"] = 
                # heatsDict[event]["numPeople"] = numPeople
                # heatsDict[event]["numHeats"] = numHeats
                # heatsDict[event]["softCutoff"] = None
                # heatsDict[event]["timeLimit"] = None
                heatsDict[event] = 0
            else:
                numHeats = math.ceil(numPeople / numPerHeat)
                heatsDict[event] = numHeats
            print("There will be {0} heats for {1} for {2} people".format(heatsDict[event], eventsDict[event], numPeople))
        else:
            userSure = False
            while not userSure:
                numPerHeat = validateInt("You have {0} competitors for {1}. How many competitors do you want in each heat? ".format(numPeople, eventsDict[event]))
                confirmed = validateYesNo("Are you sure you want {0} heats for {1} people in {2}? (Y/N) ".format(numPerHeat, numPeople, eventsDict[event]))
                if confirmed == 'y' and numPerHeat < numPeople and numPerHeat > 0:
                    userSure = True
                    numHeats = math.ceil(numPeople / numPerHeat)
                    print("There will be {0} heats for {1} for {2} people".format(numHeats, eventsDict[event], numPeople))
                    heatsDict[event] = numHeats
    return heatsDict


def customHeats(compData):
    '''
    uses psych sheet data and staff data to assign heats
    '''
    # waiting for the WCA Software Team to add psych sheet data into the JSON file


def easyHeats(compData, heatsDict):
    '''
    Goes straight down list of competitors from 1 to numPeopleInHeats
    '''
    for event in heatsDict:
        for i, person in enumerate(compData[1][event]["rounds"][0]["results"]):
            if (heatsDict[event] != 0):
                person["heat"] = (i % heatsDict[event]) + 1

    return compData


def sortHeats(assignedHeats):
    '''
    Sorts people in each event by heat number for easy scoresheet cutting and sorting
    '''
    for event in assignedHeats[1]:
        (assignedHeats[1][event]["rounds"][0]["results"]).sort(key=lambda x: x["heat"])


def makePrintableHeatSheet(assignedHeats, jsonFile):
    '''
    Gets all the heats for each competitor and turns it into a printable format
    makes a list of [name, [list of events with heat numbers]] 
        sorted by name (with events sorted by alphabetical order)
    prints to file
    '''
    # make list of dictionaries with person name and all the events
    competitorHeats = []
    for person in jsonFile["persons"]:
        tempDict = {}
        tempDict["name"] = person["name"]
        for event in assignedHeats[1]:
            for personData in assignedHeats[1][event]["rounds"][0]["results"]:
                tempDict[event] = personData["heat"]
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
    
    # print to file




def makeScoreSheets(assignedHeats, heatsDict, eventsDict):
    '''
    Creates string with HTML that contains all of the necessary 
    scoresheets for the first round of the competition
    '''
    # TODO: -add scoresheets with only 3 attempts for BLD events
    #       -remove scoresheets for FMC
    #           -remind user that they need to print those out
    #       -find better way to get cutoffs for events
    scoreSheetList = []
    notAo5Events = ["333ft", "333fm", "333bf", "666", "777", "444bf", "555bf", "333mbf"]
    for event in assignedHeats[1]:
        # hasCutoff = validateYesNo("Does {0} have a cutoff? ".format(event))
        # softCutoff = "None"
        # hardCutoff = "None"
        # if hasCutoff == "y":
        #     print("If there is no cutoff, write None")
        #     softCutoff = input("Soft cutoff for {0}? ".format(event))
        #     hardCutoff = input("Time limit for {0}? ".format(event))
        for person in assignedHeats[1][event]["rounds"][0]["results"]:
            if event in notAo5Events:
                updatedScoreSheetTable = scoresheetsHtml.mo3Table
            else:
                updatedScoreSheetTable = scoresheetsHtml.ao5Table
            # python and it's weird rules for strings
            updatedScoreSheetTable = updatedScoreSheetTable.replace("competitionName", assignedHeats[0])
            updatedScoreSheetTable = updatedScoreSheetTable.replace("eventName", eventsDict[event])
            updatedScoreSheetTable = updatedScoreSheetTable.replace("heatNumber", str(person["heat"]))
            updatedScoreSheetTable = updatedScoreSheetTable.replace("roundNumber", str(1))
            updatedScoreSheetTable = updatedScoreSheetTable.replace("competitorID", person["id"])
            updatedScoreSheetTable = updatedScoreSheetTable.replace("competitorName", person["name"])
            # updatedScoreSheetTable = updatedScoreSheetTable.replace("softCutoff", softCutoff)
            # updatedScoreSheetTable = updatedScoreSheetTable.replace("timeLimit", hardCutoff)
            scoreSheetList.append(updatedScoreSheetTable)

    scoreSheets = str.join("\n", scoreSheetList)

    return scoresheetsHtml.startHTML + scoreSheets + scoresheetsHtml.endHTML


def main():
    printMenu()

    jsonFile = getDataFile()

    compData = getCompetitionData(jsonFile)
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
    heatsDict = calcNumHeats(compData, eventsDict)

    assignedHeats = easyHeats(compData, heatsDict)
    makePrintableHeatSheet(assignedHeats, jsonFile)
    sortHeats(assignedHeats)
    newFile = makeScoreSheets(assignedHeats, heatsDict, eventsDict)
    
    webpage = open('scoresheets.html', 'w')
    webpage.write(newFile)
    
    print()
    print("HEATS HAVE BEEN GENERATED")
    print("1. Make sure screen.css is in the same folder as scoresheets.html")
    print("2. Open scoresheets.html")
    print("3. Print to file (save as PDF) with 4 sheets per page")
    print("4. If your competition has FMC: FMC scoresheets have been generated.")
    print("5. Print score sheets and cut them (everything is already sorted by heat number)")


if __name__ == '__main__':
    main()