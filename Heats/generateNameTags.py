startHTML = '''
    <html>
        <head>
            <link rel="stylesheet" type="text/css" href="nameTag.css" />
        </head>
        <body>
'''

nameTagTemplate = '''
            <table>
                <tr>
                    <td class="name">name1</td>
                    <td class="name">name2</td>
                </tr>
                <tr>
                    <td class="name">name3</td>
                    <td class="name">name4</td>
                </tr>
                <tr>
                    <td class="name">name5</td>
                    <td class="name">name6</td>
                </tr>
                <tr>
                    <td class="name">name7</td>
                    <td class="name">name8</td>
                </tr>
            </table>
'''

endHTML = '''
        </body>
    </html>
'''


staffList = []
with open("staff.txt", "r") as staffFile:
    for line in staffFile:
        staffList.append(line.strip())

competitorList = []
with open("competitorList.txt", "r") as competitorFile:
    for line in competitorFile:
        competitorList.append(line.strip())

numPeople = len(competitorList)
for person in range(numPeople):
    if competitorList[person] in staffList:
        competitorList[person] = competitorList[person] + '<br>STAFF'


output = startHTML

for person in range(0, numPeople, 8):
    nameTag = nameTagTemplate
    try:
        nameTag = nameTag.replace("name2", competitorList[person + 1])
        nameTag = nameTag.replace("name1", competitorList[person])
        nameTag = nameTag.replace("name3", competitorList[person + 2])
        nameTag = nameTag.replace("name4", competitorList[person + 3])
        nameTag = nameTag.replace("name5", competitorList[person + 4])
        nameTag = nameTag.replace("name6", competitorList[person + 5])
        nameTag = nameTag.replace("name7", competitorList[person + 6])
        nameTag = nameTag.replace("name8", competitorList[person + 7])
    except:
        continue
    output += nameTag

output += endHTML


with open("nameTags.html", "w") as f:
    print(output, file=f)