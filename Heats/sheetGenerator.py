import heatGenerator
import math
import json
import scoresheetsHtml
import sys
import pickle
import csv


def addScoreSheet(updatedScoreSheetTable, compName, allEventsDict, event,
                  person, newIDs, cutoff, timeLimit):
    updatedScoreSheetTable = updatedScoreSheetTable.replace("competitionName", compName
                                                  ).replace("eventName", allEventsDict[event]
                                                  ).replace("heatNumber", str(person[0])
                                                  ).replace("roundNumber", str(1)
                                                  # ).replace("competitorID", person["id"])
    # REMOVE WHEN CUBECOMPS TAKES JSON STUFF
                                                  ).replace("competitorID", newIDs[person[1]]
                                                  ).replace("competitorName", str(person[1])
                                                  ).replace("cutoffTime", cutoff
                                                  ).replace("timeLimit", timeLimit)
    return updatedScoreSheetTable


def addBlankScoresheet(updatedScoreSheetTable, compName):
    updatedScoreSheetTable = updatedScoreSheetTable.replace("competitionName", compName
                                                  ).replace("eventName", r"."
                                                  ).replace("heatNumber", r"."
                                                  ).replace("roundNumber", str(1)
                                                  # ).replace("competitorID", person["id"])
    # REMOVE WHEN CUBECOMPS TAKES JSON STUFF
                                                  ).replace("competitorID", r"."
                                                  ).replace("competitorName", r"."
                                                  ).replace("cutoffTime", r"."
                                                  ).replace("timeLimit", r".")
    return updatedScoreSheetTable


def makeScoreSheets(compName, assignedHeats, allEventsDict, inputData, newIDs, dataType):
    '''
    Creates string with HTML that contains all of the necessary
    score sheets for the first round of the competition
    '''
    scoreSheetList = []
    notAo5Events = ["333ft", "333fm", "333bf", "666", "777", "444bf", "555bf", "333mbf"]
    for event in assignedHeats:
        # skip FMC
        if event == "333fm":
            continue

        # set cutoff and time limit
        cutoff = inputData[event]["cutoff"]
        timeLimit = inputData[event]["timeLimit"]
        if cutoff == "":
            cutoff = "None"
        if timeLimit == "":
            timeLimit = "None"

        # add scoresheets
        for person in assignedHeats[event]:
            # figure out event format (ao5 or mo3)
            if event in notAo5Events:
                updatedScoreSheetTable = scoresheetsHtml.mo3Table
            else:
                updatedScoreSheetTable = scoresheetsHtml.ao5Table
            if person[0] is None:
                scoreSheetList.append(addBlankScoresheet(updatedScoreSheetTable, compName))
            else:
                scoreSheetList.append(addScoreSheet(updatedScoreSheetTable, compName,
                                                allEventsDict, event, person,
                                                newIDs, cutoff, timeLimit))

        # add extra blank sheets as needed so that new heats start on new page
        if len(assignedHeats[event]) % 4:
            if event in notAo5Events:
                updatedScoreSheetTable = scoresheetsHtml.mo3Table
            else:
                updatedScoreSheetTable = scoresheetsHtml.ao5Table
            for blankScoreSheet in range(4 - (len(assignedHeats[event]) % 4)):
                scoreSheetList.append(addBlankScoresheet(updatedScoreSheetTable, compName))
    scoreSheets = str.join("\n", scoreSheetList)

    return scoresheetsHtml.startHTML + scoreSheets + scoresheetsHtml.endHTML


def readAndSortHeats(inputData, dataType):
    '''
    Sorts people in each event by heat number for easy score sheet cutting and sorting
    '''
    assignedHeats = {}
    for event in inputData:
        assignedHeats[event] = []

    with open("printableGroups.csv", 'r', newline = '') as input_file:
        heatReader = csv.DictReader(input_file, delimiter=',', quotechar ='"')
        for row in heatReader:
            for event in inputData:
                if event != "333fm" and len(row[event]):
                    if dataType == 'json':
                        heatAndName = (int(row[event]), row["name"])
                    else:
                        heatAndName = (int(row[event]), row["Name"])
                    assignedHeats[event].append(heatAndName)

    # sort by heat number within each event
    for event in assignedHeats:
        assignedHeats[event].sort(key=lambda x: x[0])

    # add empty tuple to force number of entries in each group to be even
    blankTuple = (None, None)
    for event in assignedHeats:
        numPeople = 0
        prevGroupNum = 1
        for groupPersonPair in range(len(assignedHeats[event])):
            numPeople += 1
            if assignedHeats[event][groupPersonPair][0] != prevGroupNum:
                prevGroupNum = assignedHeats[event][groupPersonPair][0]
                if not numPeople % 2:
                    assignedHeats[event].insert(groupPersonPair, blankTuple)
    return assignedHeats


def printScoreCardIntro():
    '''
    Prints program instructions for user
    '''
    print("CubeToaster - Scorecard Generator")
    print("Type Ctrl-C or Ctrl-Z to quit the program at any time.")
    print("This program requires the output from heatGenerator.py to function properly. Has heatGenerator.py already been run?")


def printScoreCardEnding():
    '''
    Prints instructions for what to do after everything is done
    '''
    print("SCORECARDS HAVE BEEN GENERATED")
    print("1. Make sure screen.css is in the same folder as scoresheets.html")
    print("2. Open scoresheets.html")
    print("3. Print to file (save as PDF) with 4 sheets per page")
    print("4. Print score sheets and cut them (everything is already sorted by event and group number)")
    print()
    print("MAKE SURE COMPETITOR ID'S IN testCompetitorID.txt MATCHES CUBECOMPS COMPETITOR ID'S")


def main():
    # Print introductory prompt and confirm that heats have been generated.
    printScoreCardIntro();
    if not (heatGenerator.validateYesNo("Type y for yes, n for no. ")):
        sys.exit("Please run heatGenerator.py first!")
    # Restore output from heatGenerator.py to properly generate scoresheets. Done with help from http://stackoverflow.com/questions/6568007/how-do-i-save-and-restore-multiple-variables-in-python
    with open('objs.pickle', 'rb') as f:
        compName, allEventsDict, inputData, newIDs, dataType = pickle.load(f)

    assignedHeats = readAndSortHeats(inputData, dataType)
    # CHANGE WHEN CUBECOMPS TAKES JSON STUFF
    newFile = makeScoreSheets(compName, assignedHeats, allEventsDict, inputData, newIDs, dataType)

    # Make HTML file with all the score sheets
    webpage = open('scoresheets.html', 'w')
    webpage.write(newFile)
    print()
    printScoreCardEnding()




if __name__ == '__main__':
    main()