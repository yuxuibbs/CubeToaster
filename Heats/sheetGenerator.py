import heatGenerator
import math
import json
import scoresheetsHtml
import sys
import pickle
import csv

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

        if dataType == 'json':
            for person in assignedHeats[event]:
                # figure out event format (ao5 or mo3)
                if event in notAo5Events:
                    updatedScoreSheetTable = scoresheetsHtml.mo3Table
                else:
                    updatedScoreSheetTable = scoresheetsHtml.ao5Table
                # python and it's weird rules for strings
                updatedScoreSheetTable = updatedScoreSheetTable.replace("competitionName", compName)
                updatedScoreSheetTable = updatedScoreSheetTable.replace("eventName", allEventsDict[event])
                updatedScoreSheetTable = updatedScoreSheetTable.replace("heatNumber", str(person[0]))
                updatedScoreSheetTable = updatedScoreSheetTable.replace("roundNumber", str(1))
                # updatedScoreSheetTable = updatedScoreSheetTable.replace("competitorID", person["id"])
                # REMOVE WHEN CUBECOMPS TAKES JSON STUFF
                updatedScoreSheetTable = updatedScoreSheetTable.replace("competitorID", newIDs[person[1]])
                updatedScoreSheetTable = updatedScoreSheetTable.replace("competitorName", str(person[1]))
                updatedScoreSheetTable = updatedScoreSheetTable.replace("cutoffTime", cutoff)
                updatedScoreSheetTable = updatedScoreSheetTable.replace("timeLimit", timeLimit)
                scoreSheetList.append(updatedScoreSheetTable)
            # add extra blank sheets as needed so that new heats start on new page
            if len(assignedHeats[event]) % 4:
                if event in notAo5Events:
                    updatedScoreSheetTable = scoresheetsHtml.mo3Table
                else:
                    updatedScoreSheetTable = scoresheetsHtml.ao5Table
                for blankScoreSheet in range(4 - (len(assignedHeats[event]) % 4)):
                    updatedScoreSheetTable = updatedScoreSheetTable.replace("competitionName", compName)
                    updatedScoreSheetTable = updatedScoreSheetTable.replace("eventName", r".")
                    updatedScoreSheetTable = updatedScoreSheetTable.replace("heatNumber", r".")
                    updatedScoreSheetTable = updatedScoreSheetTable.replace("roundNumber", str(1))
                    # updatedScoreSheetTable = updatedScoreSheetTable.replace("competitorID", person["id"])
                    # REMOVE WHEN CUBECOMPS TAKES JSON STUFF
                    updatedScoreSheetTable = updatedScoreSheetTable.replace("competitorID", r".")
                    updatedScoreSheetTable = updatedScoreSheetTable.replace("competitorName", r".")
                    updatedScoreSheetTable = updatedScoreSheetTable.replace("cutoffTime", r".")
                    updatedScoreSheetTable = updatedScoreSheetTable.replace("timeLimit", r".")
                    scoreSheetList.append(updatedScoreSheetTable)
        else:
            for person in assignedHeats:
                # figure out event format (ao5 or mo3)
                if person[event] in notAo5Events:
                    updatedScoreSheetTable = scoresheetsHtml.mo3Table
                else:
                    updatedScoreSheetTable = scoresheetsHtml.ao5Table
                # python and it's weird rules for strings
                updatedScoreSheetTable = updatedScoreSheetTable.replace("competitionName", compName)
                updatedScoreSheetTable = updatedScoreSheetTable.replace("eventName", allEventsDict[event])
                updatedScoreSheetTable = updatedScoreSheetTable.replace("heatNumber", str(person[0]))
                updatedScoreSheetTable = updatedScoreSheetTable.replace("roundNumber", str(1))
                # updatedScoreSheetTable = updatedScoreSheetTable.replace("competitorID", person["id"])
                # REMOVE WHEN CUBECOMPS TAKES JSON STUFF
                updatedScoreSheetTable = updatedScoreSheetTable.replace("competitorID", newIDs[person[1]])
                updatedScoreSheetTable = updatedScoreSheetTable.replace("competitorName", str(person[1]))
                updatedScoreSheetTable = updatedScoreSheetTable.replace("cutoffTime", cutoff)
                updatedScoreSheetTable = updatedScoreSheetTable.replace("timeLimit", timeLimit)
                scoreSheetList.append(updatedScoreSheetTable)
            # add extra blank sheets as needed so that new heats start on new page
            if len(assignedHeats[event]) % 4:
                if event in notAo5Events:
                    updatedScoreSheetTable = scoresheetsHtml.mo3Table
                else:
                    updatedScoreSheetTable = scoresheetsHtml.ao5Table
                for blankScoreSheet in range(4 - (len(assignedHeats[event]) % 4)):
                    updatedScoreSheetTable = updatedScoreSheetTable.replace("competitionName", compName)
                    updatedScoreSheetTable = updatedScoreSheetTable.replace("eventName", r".")
                    updatedScoreSheetTable = updatedScoreSheetTable.replace("heatNumber", r".")
                    updatedScoreSheetTable = updatedScoreSheetTable.replace("roundNumber", str(1))
                    # updatedScoreSheetTable = updatedScoreSheetTable.replace("competitorID", person["id"])
                    # REMOVE WHEN CUBECOMPS TAKES JSON STUFF
                    updatedScoreSheetTable = updatedScoreSheetTable.replace("competitorID", r".")
                    updatedScoreSheetTable = updatedScoreSheetTable.replace("competitorName", r".")
                    updatedScoreSheetTable = updatedScoreSheetTable.replace("cutoffTime", r".")
                    updatedScoreSheetTable = updatedScoreSheetTable.replace("timeLimit", r".")
                    scoreSheetList.append(updatedScoreSheetTable)

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

    for event in assignedHeats:
        assignedHeats[event].sort(key=lambda x: x[0])

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