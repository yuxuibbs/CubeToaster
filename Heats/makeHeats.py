import math
import responseValidation
import createFiles
import getData

def specialStaffHeats(jsonFile):
    print()
    staffHeats = responseValidation.validateYesNo("Special staff heats? ")
    if staffHeats:
        print("Open competitors.txt and delete everyone that is NOT a staff member (competitors.txt should only have staff members who are competing)")
        createFiles.makeCompetitorList(jsonFile)
        while True:
            if responseValidation.validateYesNo("Type y when done. "):
                staffList = getData.getStaffList()
                break
            else:
                continue
    return staffList

def calcNumHeats(compData, eventsDict, inputData):
    '''
    Gets number of heats for each event from user
    recommended number of people per heat: ceil(1.5*numStations) to the nearest even number
    '''
    heatsDict = {}
    for event in compData[1]:
        numPeople = len(compData[1][event]["rounds"][0]["results"])
        if event == "444bf" or event == "555bf" or event == "333fm" or event == "333mbf":
            heatsDict[event]= 0
        else:
            heatsDict[event] = inputData[event]["numHeats"]
        print("There will be {0} heats for {1} for {2} people".format(heatsDict[event], eventsDict[event], numPeople))
    return heatsDict


def customHeats(compData):
    '''
    uses psych sheet data and staff data to assign heats
    '''
    # waiting for the WCA Software Team to add psych sheet data into the JSON file


def easyHeats(compData, heatsDict):
    '''
    Goes straight down list of competitors from 1 to numPeopleInHeats
    '''
    ''' TODO: later
    staff = False
    # assumes that number of people on staff is always less than 60% of the number of people in 3x3x3
    if len(staffList) < len(compData[1][event]["rounds"][0]["results"]) * 0.6:
        staff = True
    '''
    for event in heatsDict:
        for i, person in enumerate(compData[1][event]["rounds"][0]["results"]):
            if (heatsDict[event] != 0):
                person["heat"] = (i % heatsDict[event]) + 1

    return compData


def sortHeats(assignedHeats):
    '''
    Sorts people in each event by heat number for easy score sheet cutting and sorting
    '''
    for event in assignedHeats[1]:
        (assignedHeats[1][event]["rounds"][0]["results"]).sort(key=lambda x: x["heat"])
