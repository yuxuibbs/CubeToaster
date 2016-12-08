import scoresheetsHtml

def createInputFile(heatsDict):
    '''
    creates json file for users to edit number of people per heat and cutoffs
    '''
    # Need to figure out how the competition organizers want to input data

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
    with open("printableHeatSheet.txt", 'w') as f:
        for person in printableHeats:
            print(person[0], file=f)
            for event, heat in person[1]:
                print("{0:25} - {1}".format(eventsDict[event], heat), file=f)
            print(file=f)

    # print to file
    with open("competitors.txt", 'w') as f:
        for person in printableHeats:
            print(person[0], file=f)


def makeScoreSheets(assignedHeats, heatsDict, eventsDict):
    '''
    Creates string with HTML that contains all of the necessary 
    score sheets for the first round of the competition
    '''
    # TODO: -add score sheets with only 3 attempts for BLD events
    #       -remove score sheets for FMC
    #           -remind user that they need to print those out
    #       -find better way to get cutoffs for events
    scoreSheetList = []
    notAo5Events = ["333ft", "333fm", "333bf", "666", "777", "444bf", "555bf", "333mbf"]
    for event in assignedHeats[1]:
        if event == "333fm":
            continue
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
