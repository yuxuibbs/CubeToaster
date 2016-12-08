import json

def getDataFile():
    '''
    Gets file name from user and reads in the JSON
    '''
    # fileName = input('Enter file name (json):').strip()
    # TODO: get csv or excel data to get accurate competitor ID numbers
    fileName = "fake gamma.json"
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
        # remove dob and replace with initial heat number
        person['heat'] = person.pop('dob')
        person['heat'] = 0
        # put person data into a dictionary with id number as key
        persons[person["id"]] = person

    for event in jsonFile["events"]:
        results = []
        # replace id in events part of JSON with the person's data
        for person in event["rounds"][0]["results"]:
            results.append(persons[person['personId']].copy())
        results.sort(key=lambda x: x['name'].lower())
        event['rounds'][0]['results'] = results
        events[event['eventId']] = event

    return (competitionId, events)
