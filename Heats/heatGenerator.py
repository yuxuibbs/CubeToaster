import json
import math
import re


def validateInt(prompt):
    while True:
        try:
            response = int(input(prompt).strip())
            break
        except:
            continue
    return response


def validateYesNo(prompt):
    response = ""
    while not (response == 'y' or response == 'n'):
        response = input(prompt).strip().lower()
    return response


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
    # TODO: get csv data to get accurate competitor ID numbers
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
            results.append(persons[person['personId']].copy())
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
    sameNumPerHeat = validateYesNo("Same number of people for all events other than 4BLD, 5BLD, multi BLD, and FMC? (y/n) ")
    
    if sameNumPerHeat == 'y':
        numPerHeat = validateInt("How many competitors do you want in each heat? ")
        automaticHeats = True
    else:
        automaticHeats = False


    heatsDict = {}
    for event in compData[1]:
        numPeople = len(compData[1][event]["rounds"][0]["results"])
        if automaticHeats:
            if event == "444bf" or event == "555bf" or event == "333fm" or event == "333mbf":
                heatsDict[event] = numHeats = 0
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
    Gets number of heats for each event from user
    '''


def easyHeats(compData, heatsDict):
    '''
    Goes straight down list of competitors from 1 to numPeopleInHeats
    '''
    for event in heatsDict:
        print(event, heatsDict[event])
        for i, person in enumerate(compData[1][event]["rounds"][0]["results"]):
            if (heatsDict[event] != 0):
                person["heat"] = (i % heatsDict[event]) + 1

    return compData


def makeScoreSheets(finishedHeats, heatsDict):
    startHTML = '''
    <html>
    <head>
    <link rel="stylesheet" type="text/css" href="screen.css" media="screen" />
    </head>
    <body>
    '''
    
    scoreSheetTable = '''
      <table>
      <tr>
        <th colspan="5" class="CompName">competitionName</th>
      </tr>
      <tr>
        <th colspan="3" class="event">eventName</th>
        <th colspan="1" class="heat">heatNumber</th>
        <th colspan="1" class="round">roundNumber</th>
      </tr>
      <tr>
        <th colspan="1" class="personID">competitorID</th>
        <th colspan="4" class="personName">competitorName</th>
      </tr>
      <tr>
        <th colspan="3">Results</th>
        <th colspan="1">Comp</th>
        <th colspan="1">Judge</th>
      </tr>
      <tr class="attempt">
        <td colspan="1">1</td>
        <td colspan="2">insertTimeHere</td>
        <td colspan="1">initial1</td>
        <td colspan="1">initial2</td>
      </tr>
      <tr class="attempt">
        <td colspan="1">2</td>
        <td colspan="2">insertTimeHere</td>
        <td colspan="1">initial1</td>
        <td colspan="1">initial2</td>
      </tr>
      <tr class="cutoffs">
        <td colspan="2">Soft Cutoff: SOFTCUTOFF</td>
        <td colspan="1"></td>
        <td colspan="2">Hard Cutoff: HARDCUTOFF</td>
      </tr>
      <tr class="attempt">
        <td colspan="1">3</td>
        <td colspan="2">insertTimeHere</td>
        <td colspan="1">initial1</td>
        <td colspan="1">initial2</td>
      </tr>
      <tr class="attempt">
        <td colspan="1">4</td>
        <td colspan="2">insertTimeHere</td>
        <td colspan="1">initial1</td>
        <td colspan="1">initial2</td>
      </tr>
      <tr class="attempt">
        <td colspan="1">5</td>
        <td colspan="2">insertTimeHere</td>
        <td colspan="1">initial1</td>
        <td colspan="1">initial2</td>
      </tr>
      <tr class="empty">
        <td colspan="5"></td>
      </tr>
      <tr class="attempt">
        <td colspan="1">6</td>
        <td colspan="2">insertTimeHere</td>
        <td colspan="1">initial1</td>
        <td colspan="1">initial2</td>
      </tr>
      </table>
    '''
    for event in finishedHeats[1]:
        for person in finishedHeats[1][event]["rounds"][0]["results"]:
            scoreSheetTable.replace("competitionName", finishedHeats[0])
            scoreSheetTable.replace("eventName", event)
            scoreSheetTable.replace("heatNumber", str(person["heat"]))
            scoreSheetTable.replace("roundNumber", str(1))
            scoreSheetTable.replace("competitorID", person["id"])
            scoreSheetTable.replace("competitorName", person["name"])
        startHTML += scoreSheetTable
    endHTML = '''
    </body>
    </html>
    '''
    return startHTML + endHTML



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
    # print(json.dumps(finishedHeats, indent=2))
    newFile = makeScoreSheets(finishedHeats, heatsDict)
    webpage = open('output.html', 'w')
    webpage.write(newFile)



if __name__ == '__main__':
    main()