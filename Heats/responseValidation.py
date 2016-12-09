import createFiles
import responseValidation
import getData

def validateInt(prompt):
    '''
    Prompts users until they input an int
    '''
    while True:
        try:
            response = int(input(prompt).strip())
            break
        except:
            continue
    return response


def validateYesNo(prompt):
    '''
    Prompts users until they enter y or n
    '''
    response = ""
    acceptedList = ["y", "yes", "n", "no"]
    while not response in acceptedList:
        response = input(prompt).strip().lower()
    if response == "y" or response == "yes":
        return True
    else:
        return False

def validateInputFile(jsonFile):
    print("Fill out inputData.json (you can leave as many things blank as you want)")
    print("There is a recommended number of heats already listed. You can change it if you want to.")
    while True:
        
        if responseValidation.validateYesNo("Type y when done. "):
            inputData = getData.getInputInfo()
            break
        '''
        try:
            if responseValidation.validateYesNo("Type y when done. "):
                inputData = getData.getInputInfo()
            break
        except:
            print("ERROR: JSON might not be valid. Make sure it is formatted correctly and try again.")
            continue
        '''
    return inputData