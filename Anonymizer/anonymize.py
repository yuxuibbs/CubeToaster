import random
import json

# names from random name generator http://listofrandomnames.com/
names = ["Yi", "Stander", "Domonique", "Valadez", "Tona", "Samuels", "Coreen", 
         "Miera", "Haywood", "Pelaez", "Ngan", "Saragosa", "Arturo", "Poulson", 
         "Vesta", "Nott", "Vinita", "Mcconn", "Lesli", "Farish", "Trent", 
         "Ogata", "Arnulfo", "Ferranti", "Hildegard", "Gaeta", "Brittney", 
         "Byrom", "Shayla", "Igoe", "Virgilio", "Clow", "Lakesha", "Abelson", 
         "Jamee", "Laroque", "Moriah", "Athens", "Carmela", "Antonio"]

numNames = len(names)

fileName = "Michigan 2016.json"
f = open(fileName, "r")
jsonFile = json.loads(f.read())
f.close()

for person in jsonFile["persons"]:
    person['name'] = names[random.randrange(numNames)] + " " + names[random.randrange(numNames)]
    person['dob'] = 'random date'
    person['wcaId'] = str(random.randrange(1982, 2016)) + "FAKE" + str(random.randrange(100))


fakeData = open('fake.json', 'w')
fakeData.write(json.dumps(jsonFile, indent=2))