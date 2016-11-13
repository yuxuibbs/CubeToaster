import csv
import os


def printMenu():
    print('CubeToaster')
    print('Make sure the csv file exists and the file name is entered correctly.')
    print('Type QUIT or Ctrl-C to quit the program.')
    print()


def getData():
    # TODO: fix input validation
    #       figure out how to read data (SQLite database?)
    while True:
        try:
            # fileName = input('Enter file name (csv format):')
            fileName = "Michigan 2016.csv"
            if fileName.endswith('.csv') and os.path.isfile(fileName):
                with open(fileName, newline='') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        print(row)
            elif fileName.upper() == 'QUIT':
                # this is broken
                quit()
            else:
                print('Invalid file name. Try again.')
                continue
        except:
            continue


def main():
    printMenu()
    data = getData()
    print(data)

if __name__ == '__main__':
    main()