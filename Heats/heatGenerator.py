import getData
import createFiles
import makeHeats
import responseValidation

def printIntro():
    '''
    Prints program name and instructions for the user
    '''
    print("CubeToaster")
    print("Takes in a JSON file with the competition data and outputs an HTML website with all the score sheets for the competition sorted by heat number")
    print("Type Ctrl-C or Ctrl-Z (whichever one works) to quit the program if something goes wrong.")

def printEnding():
    print("HEATS HAVE BEEN GENERATED")
    print("1. Make sure screen.css is in the same folder as scoresheets.html")
    print("2. Open scoresheets.html")
    print("3. Print to file (save as PDF) with 4 sheets per page")
    print("4. Print score sheets and cut them (everything is already sorted by event and heat number)")


def main():
    printIntro()
    print()

    jsonFile = getData.getDataFile()

    # staffList = makeHeats.specialStaffHeats(jsonFile)

    compData = getData.getCompetitionData(jsonFile)

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
    createFiles.createInputFile(compData)
    print()
    inputData = responseValidation.validateInputFile(jsonFile)
    # figure out how many heats there will be for each event
    heatsDict = makeHeats.calcNumHeats(compData, eventsDict, inputData)
    # assign heats
    assignedHeats = makeHeats.easyHeats(compData, heatsDict)
    # make output files
    createFiles.makePrintableHeatSheet(assignedHeats, jsonFile, eventsDict)
    makeHeats.sortHeats(assignedHeats)
    newFile = createFiles.makeScoreSheets(assignedHeats, heatsDict, eventsDict, inputData)
    
    # make HTML file with all the score sheets
    webpage = open('scoresheets.html', 'w')
    webpage.write(newFile)
    
    print()
    printEnding()


if __name__ == '__main__':
    main()