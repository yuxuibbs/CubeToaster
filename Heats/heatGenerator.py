import csv
import os
import sqlite3
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup

'''
mimic WCA competition scoresheet or use minimum amount of data necessary (id, name, events)?
how to represent data from json?
classes? competitor class?
    id (from cubingUSA JSON)
    name
    events
        how to deal with events?
            assume all events or only make stuff for events that will be held?
    advantages: events are with the people instead of separate
how to get psych sheet data?
    beautiful soup (easy)
    wca database export (grabs a ton more data)
'''

'''
json format:
{
    "formatVersion":"CubingUSA Output",
    "competitionId":"stuff",
    "persons":[
        {
            "id":"1",
            "name":"first last",
            "wcaId":"randomString",
            "countryId":"US",
            "gender":"meh",
            "dob":"stuff"
        },
    ],
    "events":[
        {
            "eventId":"222",
            "rounds":[
                {
                    "roundId":"f",
                    "formatId":"a",
                    "results":[
                        {
                            "personId":"1"
                        },
                    ],
                    "groups":[

                    ]
                }
            ]
        },
    ]
}
'''

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


def printMenu():
    print("CubeToaster")
    print("Type Ctrl-C or Ctrl-Z (whichever one works) to quit the program.")
    print()



def getData():
    # fileName = input('Enter file name (json):').strip()
    fileName = "Michigan 2016.json"
    f = open(fileName, "r")
    file = json.loads(f.read())
    f.close()
    return file
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
def makeDataList(json_file):
    """
    Parses JSON into a data structure
    Returns (competition_id, events)
    """
    competition_id = json_file["competitionId"]
    persons = {}
    events = {}

    for person in json_file["persons"]:
        persons[person["id"]] = person

    for event in json_file["events"]:
        results = []
        for person in event["rounds"][0]["results"]:
            results.append(persons[person['personId']])
        results.sort(key=lambda x: x['name'].lower())
        event['rounds'][0]['results'] = results
        events[event['eventId']] = event
    return (competition_id, events)


def getEvents(json_file):
    eventList = list()
    for event in json_file["events"]:
        eventList.append(event["eventId"])
    return eventList

def getPsychSheet(competitionName, eventsList):
    stachuPsychSheet = "http://psychsheets.azurewebsites.net/"
    baseURL = stachuPsychSheet + "/" + competitionName + "/"
    for event in eventsList:
        url = baseURL + event
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "html.parser")
        print(url)


def main():
    printMenu()
    jsonFile = getData()
    dataList = makeDataList(jsonFile)
    print(json.dumps(dataList[1], indent=2))
    # events = getEvents(jsonFile)
    # print(events)
    # getPsychSheet("Michigan2016", events)


if __name__ == '__main__':
    main()