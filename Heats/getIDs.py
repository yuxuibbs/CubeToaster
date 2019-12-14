import heatGenerator
import json
import csv

with open("printableGroups.csv", 'r+', newline = '') as input_file:
    heatReader = csv.DictReader(input_file, delimiter=',', quotechar ='"')

    # with open("wcif.json", 'w') as f:
    #     f.write('')

    print('Open wcif.json and copy/paste the contents of https://www.worldcubeassociation.org/api/v0/competitions/{competition name}/wcif into that file')

    if heatGenerator.validateYesNo('Type y when done. ') == 'y':
        with open("wcif.json", 'r') as f:
            data = json.loads(f.read())
            people = {}
            for person in data['persons']:
                people[person["name"]] = person["registrantId"]

    for row in heatReader:
        row['ID'] = people[row['Name']]