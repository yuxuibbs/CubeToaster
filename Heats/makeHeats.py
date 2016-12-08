import math
import responseValidation

def calcNumHeats(compData, eventsDict):
    '''
    Gets number of heats for each event from user
    recommended number of people per heat: ceil(1.5*numStations) to the nearest even number
    '''
    sameNumPerHeat = responseValidation.validateYesNo("Same number of people for all events other than 4BLD, 5BLD, multi BLD, and FMC? (y/n) ")
    
    if sameNumPerHeat == 'y':
        numPerHeat = responseValidation.validateInt("How many competitors do you want in each heat? ")
        automaticHeats = True
    else:
        automaticHeats = False

    print()

    heatsDict = {}
    for event in compData[1]:
        numPeople = len(compData[1][event]["rounds"][0]["results"])
        if automaticHeats:
            if event == "444bf" or event == "555bf" or event == "333fm" or event == "333mbf":
                heatsDict[event] = 0
            else:
                numHeats = math.ceil(numPeople / numPerHeat)
                heatsDict[event] = numHeats
            print("There will be {0} heats for {1} for {2} people".format(heatsDict[event], eventsDict[event], numPeople))
        else:
            userSure = False
            while not userSure:
                numPerHeat = responseValidation.validateInt("You have {0} competitors for {1}. How many competitors do you want in each heat? ".format(numPeople, eventsDict[event]))
                confirmed = responseValidation.validateYesNo("Are you sure you want {0} heats for {1} people in {2}? (Y/N) ".format(numPerHeat, numPeople, eventsDict[event]))
                if confirmed == 'y' and numPerHeat < numPeople and numPerHeat > 0:
                    userSure = True
                    numHeats = math.ceil(numPeople / numPerHeat)
                    print("There will be {0} heats for {1} for {2} people".format(numHeats, eventsDict[event], numPeople))
                    heatsDict[event] = numHeats
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
