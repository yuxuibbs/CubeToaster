import heatGenerator
import math
import json
import scoresheetsHtml
import sys
import pickle

def makeScoreSheets(assignedHeats, heatsDict, eventsDict, inputData, newIDs):
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
            # updatedScoreSheetTable = updatedScoreSheetTable.replace("competitorID", person["id"])
            # REMOVE WHEN CUBECOMPS TAKES JSON STUFF
            updatedScoreSheetTable = updatedScoreSheetTable.replace("competitorID", newIDs[person["name"]])
            updatedScoreSheetTable = updatedScoreSheetTable.replace("competitorName", person["name"])
            updatedScoreSheetTable = updatedScoreSheetTable.replace("cutoffTime", cutoff)
            updatedScoreSheetTable = updatedScoreSheetTable.replace("timeLimit", timeLimit)
            scoreSheetList.append(updatedScoreSheetTable)

    scoreSheets = str.join("\n", scoreSheetList)

    return scoresheetsHtml.startHTML + scoreSheets + scoresheetsHtml.endHTML

def sortHeats(assignedHeats):
    '''
    Sorts people in each event by heat number for easy score sheet cutting and sorting
    '''
    for event in assignedHeats[1]:
        (assignedHeats[1][event]["rounds"][0]["results"]).sort(key=lambda x: x["heat"])

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
    #Restore output from heatGenerator.py to properly generate scoresheets. Done with help from http://stackoverflow.com/questions/6568007/how-do-i-save-and-restore-multiple-variables-in-python
    with open('objs.pickle', 'rb') as f:
        assignedHeats, heatsDict, eventsDict, inputData, newIDs = pickle.load(f)
    sortHeats(assignedHeats)
    # CHANGE WHEN CUBECOMPS TAKES JSON STUFF
    newFile = makeScoreSheets(assignedHeats, heatsDict, eventsDict, inputData, newIDs)
   
    # make HTML file with all the score sheets
    webpage = open('scoresheets.html', 'w')
    webpage.write(newFile)
    print()
    printScoreCardEnding()



if __name__ == '__main__':
    main()