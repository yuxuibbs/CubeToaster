import csv
import os
import sqlite3
import json
from urllib.request import urlopen
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

eventsDict = {"222"   : "2x2 Cube",
              "222bf" : "2x2 Cube: Blindfolded",
              "333"   : "Rubik's Cube",
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
'''

'''
class Competitor():
    def __init__(self, id, name, wcaId, countryId, events):
        self.id = 
        self.name =
        self.wcaId =
        self.countryId =
        self.events =
'''

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
def makeDataList(file):
    data = []
    data.append(file["competitionId"])
    # this doesn't work
    for event in file["events"]:
        for person in event["rounds"][0]["results"]
            print(person)
    for person in file["persons"]:
        # if person["id"] in file["events"]
        templist = [person['name'], person['id'], person['wcaId']]
    return data

def getEvents(file):
    eventList = list()
    for event in file["events"]:
        eventList.append(event["eventId"])
    return eventList

def getPsychSheet(competitionName, eventsList):
    stachuPsychSheet = "http://psychsheets.azurewebsites.net/"
    baseURL = stachuPsychSheet + competitionName
    # for event in eventsList:


def main():
    printMenu()
    jsonFile = getData()
    dataList = makeDataList(jsonFile)
    print(dataList)
    print(getEvents(jsonFile))

if __name__ == '__main__':
    main()