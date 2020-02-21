import heatGenerator
import json
import csv

info = []

with open("printableGroups.csv", 'r', newline = '') as input_file:
    heatReader = csv.DictReader(input_file, delimiter=',', quotechar ='"')

    print('Open wcif.json and copy/paste the contents of https://www.worldcubeassociation.org/api/v0/competitions/{competition name}/wcif into that file')

    if heatGenerator.validateYesNo('Type y when done. ') == 'y':
        with open("wcif.json", 'r') as f:
            data = json.loads(f.read())
            people = {}
            for person in data['persons']:
                people[person["name"]] = person["registrantId"]

    for row in heatReader:
        row['ID'] = people[row['Name']]
        info.append(row)

with open("printableGroups.csv", 'w', newline = '') as output_file:
    writer = csv.DictWriter(output_file, fieldnames = ['Name', 'ID', '222', '333', '333oh', '333bf', '333fm', '333ft', '333mbf', '444', '444bf', '555', '555bf', '666', '777', 'clock', 'minx', 'pyram', 'skewb', 'sq1'])
    writer.writeheader()
    writer.writerows(info)