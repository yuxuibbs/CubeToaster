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
    print('CubeToaster - Heat Generator')
    print('Takes in a JSON or CSV file with the competition data and outputs an HTML website with all the score sheets for the competition sorted by heat number')
    print('Type Ctrl-C or Ctrl-Z (whichever one works) to quit the program if something goes wrong.')


def printEnding():
    '''
    Prints instructions for what to do after everything is done
    '''
    print('GROUPS HAVE BEEN GENERATED')
    print('1. Open printableGroups.csv to view group assignments.')
    print('2. Make sure people with the same first name (or similar names) are not in the same group. You can edit the assignments in the csv file before generating scorecards and still have correct scorecards.')
    print('3. To generate scorecards, run sheetGenerator.py and follow prompts')


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
    response = ''
    acceptedList = ['y', 'yes', 'n', 'no']
    while not response in acceptedList:
        response = input(prompt).strip().lower()
    if response == 'y' or response == 'yes':
        return True
    else:
        return True


def validateInputFile():
    print('Fill out inputData.json (you can leave as many things blank as you want)')
    print('There is a recommended number of groups already listed. You can change it if you want to.')
    print('Everything is based on numGroups (changing numPeople or peoplePerGroup will not change the number of people in each group.)')

    while True:
        if validateYesNo('Type y when done. '):
            f = open('inputData.json', 'r')
            inputData = json.loads(f.read())
            f.close()
            print()
            break
    return inputData


################################################################################
# Data Retrieval
def getJSONDataFile():
    '''
    Gets file name from user and reads in the JSON file
    '''
    fileName = input('Enter file name (json): ').strip()
    if not fileName.endswith('.json'):
        fileName = fileName + '.json'
    f = open(fileName, 'r')
    # read json data
    fileData = json.loads(f.read())
    f.close()
    return fileData

def getCompEvents(header, eventsDict):
    '''
    Gets events list from header of csv file
    '''
    events = {}
    for event in header:
        if event in eventsDict:
            events[event] = eventsDict[event]
    return events


def getCSVDataFile():
    '''
    Gets file name from user
    '''
    fileName = input('Enter file name (csv): ').strip()
    if not fileName.endswith('.csv'):
        fileName = fileName + '.csv'
    return fileName

def readCSVDataFile(fileName, eventsList):
    '''
    Read CSV file and make data structure
    '''
    # initialize data structure
    fileData = {}

    with open(fileName, 'r', newline = '') as input_file:
        dataReader = csv.DictReader(input_file, delimiter=',', quotechar ="'")
        compEventsDict = getCompEvents(dataReader.fieldnames, eventsList)
        # predict cubecomps ID
        predictedID = 1
        for row in dataReader:
            # use competitor's name as the key
            personName = row['Name'].strip()
            fileData[personName] = row
            fileData[personName]['firstName'] = personName.split(' ')[0]
            fileData[personName]['ID'] = str(predictedID)
            fileData[personName]['Staff'] = 0
            predictedID += 1
            # delete unneeded data
            del fileData[personName]['IP']
            del fileData[personName]['Country']
            del fileData[personName]['WCA ID']
            del fileData[personName]['Status']
            del fileData[personName]['Email']
            del fileData[personName]['Birth Date']
            del fileData[personName]['Guests']
            del fileData[personName]['Gender']
    return [fileData, compEventsDict]


def getStaffList(personList, fileType):
    '''
    Makes staff.txt with a list of all the competitors in the competition so
    user can specify staff members
    '''
    with open('staff.txt', 'w') as f:
        with open('competitorList.txt', 'w') as comp:
            if fileType == 'json':
                for person in personList:
                    print(person['name'], file=f)
                    print(person['name'], file=comp)
            else:
                for person in personList:
                    print(person, file=f)
                    print(person, file=comp)

    print('Open staff.txt and delete anyone that is NOT on staff')

    while True:
        if validateYesNo('Type y when done. '):
            return readStaffList()


def getCompetitionData(jsonFileData):
    '''
    Parses JSON into a data structure
    Returns (competitionId, compData)
    '''
    # let user choose competition name
    compName = input('Input competition name (this is the name that will appear on all score cards): ')
    jsonFileData['competitionId'] = compName

    competitionId = jsonFileData['competitionId']
    persons = {}
    compData = {}

    staffList = getStaffList(jsonFileData['persons'], 'json')

    for person in jsonFileData['persons']:
        # remove unnecessary data (WCA ID, country, gender, and dob)
        del person['wcaId']
        del person['countryId']
        del person['gender']
        del person['dob']
        # make sure name is in title case
        person['name'] = person['name'].title()
        # initialize heat number
        person['heat'] = 0
        if person['name'] in staffList:
            person['staff'] = 1
        else:
            person['staff'] = 0
        # put person data into a dictionary with id number as key
        persons[person['id']] = person

    for event in jsonFileData['events']:
        results = []
        # replace id in events part of JSON with the person's data
        for person in event['rounds'][0]['results']:
            try:
                results.append(persons[person['personId']].copy())
            except:
                print('POSSIBLE ERROR: Make sure all registered competitors are in competitors.txt')
        results.sort(key=lambda x: (-x['staff'], x['name'].lower()))
        event['rounds'][0]['results'] = results
        compData[event['eventId']] = event

    return (competitionId, compData)


def readStaffList():
    staff = []
    with open('staff.txt', 'r') as f:
        for line in f:
            staff.append(line.strip())
    return staff


################################################################################
# Everything related to making/calculating heats
def calcNumHeats(compData, inputData, dataType):
    '''
    Gets number of heats for each event from user
    recommended number of people per heat: ceil(1.5*numStations) to the nearest even number
    '''
    numHeatsPerEvent = {}
    if dataType == 'json':
        for event in compData[1]:
            numPeople = len(compData[1][event]['rounds'][0]['results'])
            if event == '333fm' or event == '333mbf':
                numHeatsPerEvent[event] = 1
            else:
                numHeatsPerEvent[event] = inputData[event]['numGroups']
            if numHeatsPerEvent[event] == 1:
                print('There will be 1 group for {0} for {1} people'.format(event, numPeople))
            else:
                print('There will be {0} groups for {1} for {2} people'.format(numHeatsPerEvent[event], event, numPeople))
    else:
        for event in compData:
            numPeople = compData[event]
            if event == '333fm' or event == '333mbf':
                numHeatsPerEvent[event] = 1
            else:
                numHeatsPerEvent[event] = inputData[event]['numGroups']
            if numHeatsPerEvent[event] == 1:
                print('There will be 1 group for {0} for {1} people'.format(event, numPeople))
            else:
                print('There will be {0} groups for {1} for {2} people'.format(numHeatsPerEvent[event], event, numPeople))
    return numHeatsPerEvent


def easyHeats(compData, numHeatsPerEvent, numPeopleDict, dataType):
    '''
    Goes straight down list of competitors from 1 to numPeopleInHeats
    '''
    ''' TODO: later
    staff = False
    # assumes that number of people on staff is always less than 60% of the number of people in 3x3x3
    if len(staffList) < len(compData[1][event]['rounds'][0]['results']) * 0.6:
        staff = True
    '''
    # print("numHeatsPerEvent", numHeatsPerEvent)
    if dataType == 'json':
        for event in numHeatsPerEvent:
            for i, person in enumerate(compData[1][event]['rounds'][0]['results']):
                if (numHeatsPerEvent[event] != 0):
                    person['heat'] = (i % numHeatsPerEvent[event]) + 1
    else:
        for event in numHeatsPerEvent:
            # event has more than 1 heat
            if numHeatsPerEvent[event] > 1:
                participantNumber = 0
                for competitor in compData:
                    # competitor is registered for this event
                    if event in competitor:
                        competitor[event] = (participantNumber % numHeatsPerEvent[event]) + 1
                        participantNumber += 1
    return compData


def makeCompetitorList(jsonFile):
    '''
    Creates txt file with all of the competitors at the competition
    '''
    # print to file
    with open('competitors.txt', 'w') as f:
        for person in jsonFile['persons']:
            print(person['name'], file=f)

def addStaffData(compData, staffList):
    for person in staffList:
        compData[person]['Staff'] = 1

def numPeoplePerEvent(compData, eventsList):
    # initialize dictionary
    peoplePerEvent = {}
    for event in eventsList:
        peoplePerEvent[event] = 0
    # count number of people in each event
    for person in compData:
        for event in eventsList:
            if compData[person][event] == '1':
                peoplePerEvent[event] += 1
            else:
                del compData[person][event]

    return peoplePerEvent

################################################################################
# Create output files
def createInputFile(compData, dataType):
    '''
    creates json file for users to edit number of people per heat and cutoffs
    '''
    data = {}
    fastEvents = ['222', '333', '333oh', 'skewb', 'pyram']

    numStations = validateInt('How many timing stations will you be using per stage? ')

    if dataType == 'json':
        for event in compData[1]:
            inputData = {}
            numPeople = len(compData[1][event]['rounds'][0]['results'])

            if event in fastEvents:
                recommendNumHeats = round(numPeople / (1.7 * numStations))
            else:
                recommendNumHeats = round(numPeople / (1.5 * numStations))
            if recommendNumHeats < 1:
                recommendNumHeats = 1

            inputData['numPeople'] = numPeople
            inputData['numGroups'] = recommendNumHeats
            inputData['cutoff'] = ''
            inputData['timeLimit'] = ''
            inputData['peoplePerGroup'] = numPeople / recommendNumHeats
            # inputData['usePsychSheet?'] = 'no'
            data[event] = inputData
    else:
        for event in compData:
            inputData = {}
            numPeople = compData[event]

            if event in fastEvents:
                recommendNumHeats = round(numPeople / (1.7 * numStations))
            else:
                recommendNumHeats = round(numPeople / (1.5 * numStations))
            if recommendNumHeats < 1:
                recommendNumHeats = 1

            inputData['numPeople'] = numPeople
            inputData['numGroups'] = recommendNumHeats
            inputData['cutoff'] = ''
            inputData['timeLimit'] = ''
            inputData['peoplePerGroup'] = numPeople / recommendNumHeats
            # inputData['usePsychSheet?'] = 'no'
            data[event] = inputData

    with open('inputData.json', 'w') as f:
        print(json.dumps(data, indent=4), file=f)


def makePrintableHeatSheet(assignedHeats, inputFile, eventsDict, dataType):
    '''
    Gets all the heats for each competitor and turns it into a printable format
    Makes a list of [name, [list of events with heat numbers]]
        sorted by name (with events sorted by alphabetical order)
    outputs:
        file with everyone's heat numbers on it
        file with everyone's names on it (for use in staff stuff later)
    '''
    if dataType == 'json':
        # make list of dictionaries with person name and all the events
        competitorHeats = []
        for person in inputFile['persons']:
            tempDict = {}
            tempDict['name'] = person['name']
            for event in assignedHeats[1]:
                for personData in assignedHeats[1][event]['rounds'][0]['results']:
                    if person['name'] == personData['name']:
                        heatNum = personData['heat']
                        tempDict[event] = heatNum
            if tempDict not in competitorHeats:
                competitorHeats.append(tempDict)

        # make competitorHeats sortable by event name
        printableHeats = []
        for competitor in competitorHeats:
            tempList = []
            for key, value in competitor.items():
                if key != 'name':
                    tempTuple = ()
                    tempTuple = (key, value)
                    tempList.append(tempTuple)
            printableHeats.append([competitor['name'], tempList])

        for person in printableHeats:
            person[1].sort(key=lambda x: x[0])
        printableHeats.sort()

        # sort by first name
        competitorHeats.sort(key=lambda x: x['name'])
        # print heat sheet to csv file
        with open('printableGroups.csv', 'w', newline='') as f:
            columnNames = ['name'] + list(eventsDict.keys())
            heatWriter = csv.DictWriter(f, fieldnames=columnNames, delimiter=',')
            heatWriter.writeheader()
            for person in competitorHeats:
                heatWriter.writerow(person)

        # REMOVE WHEN CUBECOMPS TAKES JSON STUFF
        newIDs = {}
        newNum = 1
        for person in printableHeats:
            newIDs[person[0]] = str(newNum)
            newNum += 1
        with open('testCompetitorID.txt', 'w') as f:
            for person in printableHeats:
                print(person[0], newIDs[person[0]], file=f)
        return newIDs
    else:
        # sort by first name
        assignedHeats.sort(key=lambda x: x['Name'])
        # REMOVE WHEN CUBECOMPS TAKES JSON STUFF
        newIDs = {}
        newNum = 1
        for person in assignedHeats:
            newIDs[person['Name']] = str(person['ID'])
        with open('testCompetitorID.txt', 'w') as f:
            for person in assignedHeats:
                print(person, newIDs[person['Name']], file=f)
        # print heat sheet to csv file
        with open('printableGroups.csv', 'w', newline='') as f:
            columnNames = ['Name', 'firstName'] + list(eventsDict.keys())
            heatWriter = csv.DictWriter(f, fieldnames=columnNames, delimiter=',')
            heatWriter.writeheader()
            for person in assignedHeats:
                # del person['firstName']
                del person['Staff']
                del person['ID']
                heatWriter.writerow(person)
        return newIDs


################################################################################
def jsonHeats(allEventsDict, dataType):
    jsonFileData = getJSONDataFile()

    compData = getCompetitionData(jsonFileData)

    # get user input to make heats
    createInputFile(compData, dataType)
    print()

    inputData = validateInputFile()
    # figure out how many heats there will be for each event
    numHeatsPerEvent = calcNumHeats(compData, inputData, dataType)
    # assign heats
    assignedHeats = easyHeats(compData, numHeatsPerEvent, None, dataType)

    # make output files for heats
    # CHANGE WHEN CUBECOMPS TAKES JSON STUFF
    newIDs = makePrintableHeatSheet(assignedHeats, jsonFileData, allEventsDict, dataType)

    # Save variables to files for sheetGenerator.py to read. Done with help from http://stackoverflow.com/questions/6568007/how-do-i-save-and-restore-multiple-variables-in-python
    with open('objs.pickle', 'wb') as f:
        pickle.dump([assignedHeats[0], allEventsDict, inputData, newIDs, dataType], f)


def csvHeats(allEventsDict, dataType):
    fileName = getCSVDataFile()
    [compData, compEventsDict] = readCSVDataFile(fileName, allEventsDict)

    # let user choose competition name
    compName = input('Input competition name (this is the name that will appear on all score cards): ')

    # get list of staff members
    staffList = getStaffList(compData, dataType)
    addStaffData(compData, staffList)

    # figure out how many people are in each event
    numPeopleDict = numPeoplePerEvent(compData, compEventsDict)
    # print("numPeopleDict:", numPeopleDict)
    # get user input to make heats
    createInputFile(numPeopleDict, dataType)
    print()
    inputData = validateInputFile()

    # figure out how many heats there will be for each event
    numHeatsPerEvent = calcNumHeats(numPeopleDict, inputData, dataType)

    # convert compData into list of dictionaries so it is sortable
    compDataList = []
    for person in compData:
        compDataList.append(compData[person])
    # sort data so that staff members are first
    compDataList.sort(key=lambda x: (-x['Staff'], x['firstName'].lower()))

    # assign heats
    assignedHeats = easyHeats(compDataList, numHeatsPerEvent, numPeopleDict, dataType)

    # make output files for heats
    # CHANGE WHEN CUBECOMPS TAKES JSON STUFF
    newIDs = makePrintableHeatSheet(assignedHeats, fileName, allEventsDict, dataType)

    # Save variables to files for sheetGenerator.py to read. Done with help from http://stackoverflow.com/questions/6568007/how-do-i-save-and-restore-multiple-variables-in-python
    with open('objs.pickle', 'wb') as f:
        pickle.dump([compName, allEventsDict, inputData, newIDs, dataType], f)


################################################################################
# Main
def main():
    printIntro()
    print()

    allEventsDict = {"222"   : "2x2 Cube",
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

    if validateYesNo('Are you using a json file? (y or n) '):
        dataType = 'json'
        jsonHeats(allEventsDict, dataType)
    else:
        dataType = 'csv'
        csvHeats(allEventsDict, dataType)

    print()
    printEnding()


if __name__ == '__main__':
    main()