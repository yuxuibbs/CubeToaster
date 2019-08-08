from flask import Flask, request, render_template, redirect, url_for, flash, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectMultipleField, widgets, FileField
from wtforms.validators import Required
import os
import pandas as pd
import numpy as np
import jellyfish



#################################################################################
# Configurations
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'cubetoaster'

allEventsDict = {"222"   : "2x2 Cube",
                 "333"   : "Rubik's Cube",
                 "333oh" : "Rubik's Cube: One-Handed",
                 "333bf" : "Rubik's Cube: Blindfolded",
                 "333fm" : "Rubik's Cube: Fewest moves",
                 "333ft" : "Rubik's Cube: With feet",
                 "333mbf": "Rubik's Cube: Multiple Blindfolded",
                 "444"   : "4x4 Cube",
                 "444bf" : "4x4 Cube: Blindfolded",
                 "555"   : "5x5 Cube",
                 "555bf" : "5x5 Cube: Blindfolded",
                 "666"   : "6x6 Cube",
                 "777"   : "7x7 Cube",
                 "clock" : "Rubik's Clock",
                 "minx"  : "Megaminx",
                 "pyram" : "Pyraminx",
                 "skewb" : "Skewb",
                 "sq1"   : "Square-1"}


input_file = '/home/yuxuan/CubeToaster/Heats/ImaginationStation.csv'

num_heats = {'222'   : 4,
             '333'   : 8,
             '333oh' : 2,
             '555'   : 3,
             '666'   : 2,
             'minx'  : 2
            }


#################################################################################
# Forms

# enable checkboxes so user can select multiple items
class CheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label = False)
    option_widget = widgets.CheckboxInput()

class RegistrationForm(FlaskForm):
    file = FileField('Registration file from WCA website:', validators = [Required()])
    submit = SubmitField('Submit')

class UserInputForm(FlaskForm):
    compName = StringField('Competition Name:', validators = [Required()])
    numStations = IntegerField('Number of timing/judging stations per stage:', validators = [Required()])
    staff = CheckboxField('Select staff members:')


# upload file
# detect file type
# read file
# get data from file
# calculate default number of heats
# get user input 
#   competition name
#       string
#   staff members
#       checkbox?
#   number of heats
#       arrow thingys that are prepopulated with recommended values
#       use javascript to dynamically change values?
# calculate actual number of heats
# assign heats
# reassign IDs
# make printable heat sheet
# display printable heat sheet
# make printable scoresheets
# display printable scoresheets


#################################################################################
# Helper functions

def create_heats(df, event, num_heats):
    counter = 0
    for row_num, registration_status in enumerate(df[event]):
        if registration_status != '0':
            df.loc[row_num, event] = counter % num_heats + 1
            counter += 1

def read_input_file(input_file):
    comp_events = []
    df = pd.read_csv(input_file, dtype=str, sep=',').drop(['Status', 'Country', 'Birth Date', 'Gender', 'Email', 'Guests', 'IP'], axis=1)
    # print(text)

    df['staff'] = 0

    for event in allEventsDict:
        if event in df:
            comp_events.append(event)
            create_heats(df, event, num_heats[event])

    df['FirstName'] = (df['Name'].str.split(expand=True)[0])
    df['MRA'] = df['FirstName'].apply(jellyfish.match_rating_codex)
    import sys
    print(sys.getsizeof(df))
    print(df.head(50))

    for event in comp_events:
        grouped_df = df.groupby(event)
        for key, item in grouped_df:
            if key != '0':
                print(key)
                print(grouped_df.get_group(key)[['Name', event, 'MRA']].sort_values(by='MRA'))
                print()
                print()
    return df
###############################################################################
## Routes and view functions

@app.route('/', methods = ['GET', 'POST'])
def home():
    registration_form = RegistrationForm()
    user_input_form = UserInputForm
    if form.validate_on_submit():
        entered_filename = request.files['file'].filename
        if len(entered_filename.split('.')) > 1 and entered_filename.split('.')[1] == "csv":
            input_file = request.files['file']
            df = read_input_file(input_file)

        return render_template('view_heats.html', form=user_input_form, output=df)
    return render_template('index.html', form=registration_form)

# @app.route('/userInput', methods = ['GET', 'POST'])
# def getInput():
#     form = UserInputForm()





if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = int(os.getenv('PORT', 5001)))
