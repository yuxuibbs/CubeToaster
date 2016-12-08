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
    while not (response == 'y' or response == 'n'):
        response = input(prompt).strip().lower()
    return response
