import csv

def getCSVDataFile():
    fileName = input('Enter file name (csv): ').strip()
    if not fileName.endswith('.csv'):
        fileName = fileName + '.csv'
    return fileName

def readCSVDataFile(fileName):
    fileData = {}

    with open(fileName, 'r', newline = '') as input_file:
        dataReader = csv.DictReader(input_file, delimiter=',', quotechar ="'")
        eventsList = dataReader.fieldnames
        with open('printableGroups.txt', 'w', newline="") as f:
            for row in dataReader:
                print(row["Name"], file=f)
                for event in eventsList[1:]:
                    if row[event]:
                        print(event + ": " + row[event], file=f)
                print(file=f)


inputFile = getCSVDataFile()
readCSVDataFile(inputFile)

