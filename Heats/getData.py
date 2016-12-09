import json

def getDataFile():
    '''
    Gets file name from user and reads in the JSON
    '''
    fileName = input('Enter file name (json): ').strip()
    if not fileName.endswith(".json"):
        fileName = fileName + ".json"
    # TODO: get csv or excel data to get accurate competitor ID numbers
    f = open(fileName, "r")
    fileData = json.loads(f.read())
    f.close()
    return fileData


def getCompetitionData(jsonFile):
    """
    Parses JSON into a data structure
    Returns (competitionId, events)
    """
    competitionId = jsonFile["competitionId"]
    persons = {}
    events = {}

    for person in jsonFile["persons"]:
        # remove unnecessary data (WCA ID, country, gender, and dob)
        del person["wcaId"]
        del person["countryId"]
        del person["gender"]
        del person["dob"]
        # make sure name is in title case
        person["name"] = person["name"].title()
        # initialize heat number
        person["heat"] = 0
        # put person data into a dictionary with id number as key
        persons[person["id"]] = person

    for event in jsonFile["events"]:
        results = []
        # replace id in events part of JSON with the person's data
        for person in event["rounds"][0]["results"]:
            try:
                results.append(persons[person["personId"]].copy())
            except:
                print("POSSIBLE ERROR: Make sure all registered competitors are in competitors.txt")
        results.sort(key=lambda x: x["name"].lower())
        event["rounds"][0]["results"] = results
        events[event["eventId"]] = event

    return (competitionId, events)

def getStaffList():
    staff = []
    with open("competitors.txt", "r") as f:
        for line in f:
            staff.append(line.strip())
    return staff

def getInputInfo():
    f = open("inputData.json", "r")
    inputData = json.loads(f.read())
    f.close()
    return inputData