import scoresheetsHtml
import json
import responseValidation
import math

def makeCompetitorList(jsonFile):
    '''
    Creates txt file with all of the competitors at the competition
    '''
    # print to file
    with open("competitors.txt", "w") as f:
        for person in jsonFile["persons"]:
            print(person["name"], file=f)

def createInputFile(compData):
    '''
    creates json file for users to edit number of people per heat and cutoffs
    '''
    data = {}
    fastEvents = ["222", "333", "333oh", "skewb", "pyram"]

    numStations = responseValidation.validateInt("How many timing stations will you be using per stage? ")
    
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
        inputData["numHeats"] = recommendNumHeats
        inputData["cutoff"] = ""
        inputData["timeLimit"] = ""
        inputData["peoplePerHeat"] = numPeople/recommendNumHeats
        
        data[event] = inputData

    with open("inputData.json", "w") as f:
        print(json.dumps(data, indent=4), file=f)


def makePrintableHeatSheet(assignedHeats, jsonFile, eventsDict):
    '''
    Gets all the heats for each competitor and turns it into a printable format
    Makes a list of [name, [list of events with heat numbers]] 
        sorted by name (with events sorted by alphabetical order)
    outputs a file with everyone's heat numbers on it
    '''
    # make list of dictionaries with person name and all the events
    competitorHeats = []
    for person in jsonFile["persons"]:
        tempDict = {}
        tempDict["name"] = person["name"]
        for event in assignedHeats[1]:
            for personData in assignedHeats[1][event]["rounds"][0]["results"]:
                if person["name"] == personData["name"]:
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
    with open("printableHeatSheet.txt", "w") as f:
        for person in printableHeats:
            print(person[0], file=f)
            for event, heat in person[1]:
                print("{0:25} - {1}".format(eventsDict[event], heat), file=f)
            print(file=f)

    # print to file
    with open("competitors.txt", "w") as f:
        for person in printableHeats:
            print(person[0], file=f)


def makeScoreSheets(assignedHeats, heatsDict, eventsDict, inputData):
    '''
    Creates string with HTML that contains all of the necessary 
    score sheets for the first round of the competition
    '''
    scoreSheetList = []
    notAo5Events = ["333ft", "333fm", "333bf", "666", "777", "444bf", "555bf", "333mbf"]
    for event in assignedHeats[1]:
        if event == "333fm":
            continue
        cutoff = inputData[event]["cutoff"]
        timeLimit = inputData[event]["timeLimit"]
        if cutoff == "":
            cutoff = "None"
        if timeLimit == "":
            timeLimit = "None"
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
            updatedScoreSheetTable = updatedScoreSheetTable.replace("cutoffTime", cutoff)
            updatedScoreSheetTable = updatedScoreSheetTable.replace("timeLimit", timeLimit)
            scoreSheetList.append(updatedScoreSheetTable)

    scoreSheets = str.join("\n", scoreSheetList)

    return scoresheetsHtml.startHTML + scoreSheets + scoresheetsHtml.endHTML
