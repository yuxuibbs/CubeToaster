from flask import Flask, request, render_template, redirect, url_for, flash, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, widgets
from wtforms.validators import Required
import os
import csv
import json
import requests
# import jellyfish



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

startHTML = '''
  <html>
    <head>
      <style>
        table {
          border-collapse: collapse;
          height: 100%;
          width: 100%;
        }

        table, th, td {
          border: 3px solid black;
        }

        @media print {
          table {
            page-break-after: always;
          }
        }

        .cutoffs td {
          border: 0;
          font-weight: bold;
        }

        .compName {
          font-size: 48pt;
          font-weight: bold;
        }

        .labels {
          font-size: 24pt;
          font-weight: bold;
        }

        .attempt {
          font-size: 36pt;
          font-weight: bold;
          text-align: center;
        }

        .event, .personID, .scrambler {
          font-size: 24pt;
          font-weight: bold;
          width: 60px;
        }

        .round, .heat {
          font-size: 24pt;
          font-weight: bold;
        }

        .personName {
          font-size: 40pt;
          font-weight: bold;
        }

        .attemptNumber {
          width: 60px;
        }

        .initial {
          width: 100px;
        }
      </style>
    </head>
    <body>
'''

ao5Table = '''
      <table>
        <tr>
          <th colspan="6" class="compName">competitionName</th>
        </tr>
        <tr>
          <th colspan="1" class="personID"></th>
          <th colspan="3" class="event">eventName</th>
          <th colspan="1" class="heat">G: </th>
          <th colspan="1" class="round">R: roundNumber</th>
        </tr>
        <tr>
          <th colspan="6" class="personName">competitorName</th>
        </tr>
        <tr class="labels">
          <th colspan="1" class="scrambler">Scr</th>
          <th colspan="1" class="attemptNumber">#</th>
          <th colspan="2">Results</th>
          <th colspan="1" class="initial">Judge</th>
          <th colspan="1" class="initial">Comp</th>
        </tr>
        <tr class="attempt">
          <td colspan="1"> </td>
          <td colspan="1">1</td>
          <td colspan="2"> </td>
          <td colspan="1"> </td>
          <td colspan="1"> </td>
        </tr>
        <tr class="attempt">
          <td colspan="1"> </td>
          <td colspan="1">2</td>
          <td colspan="2"> </td>
          <td colspan="1"> </td>
          <td colspan="1"> </td>
        </tr>
        <tr class="cutoffs">
          <td colspan="1"></td>
          <td colspan="1"></td>
          <td colspan="1">Cutoff: cutoffTime</td>
          <td colspan="1">Time Limit: timeLimit</td>
          <td colspan="1"></td>
          <td colspan="1"></td>
        </tr>
        <tr class="attempt">
          <td colspan="1"> </td>
          <td colspan="1">3</td>
          <td colspan="2"> </td>
          <td colspan="1"> </td>
          <td colspan="1"> </td>
        </tr>
        <tr class="attempt">
          <td colspan="1"> </td>
          <td colspan="1">4</td>
          <td colspan="2"> </td>
          <td colspan="1"> </td>
          <td colspan="1"> </td>
        </tr>
        <tr class="attempt">
          <td colspan="1"> </td>
          <td colspan="1">5</td>
          <td colspan="2"> </td>
          <td colspan="1"> </td>
          <td colspan="1"> </td>
        </tr>
        <tr class="empty">
          <td colspan="6"></td>
        </tr>
        <tr class="attempt">
          <td colspan="1"> </td>
          <td colspan="1">E</td>
          <td colspan="2"> </td>
          <td colspan="1"> </td>
          <td colspan="1"> </td>
        </tr>
      </table>
'''

endHTML = '''
    </body>
  </html>
'''


#################################################################################
# Forms
class RegistrationForm(FlaskForm):
    # compId = StringField('Competition ID from WCA website:', validators = [Required()])
    compName = StringField('Competition name to use in scorecards:', validators = [Required()])
    roundNum = StringField('Round number:', validators = [Required()])
    event = StringField('Event:', validators = [Required()])
    cutoff = StringField('Cutoff:', validators = [Required()])
    timeLimit = StringField('Time limit:', validators = [Required()])
    names = StringField('Insert list of people separated by comma:', validators = [Required()])
    submit = SubmitField('Submit')

class WCIFInputForm(FlaskForm):
    compId = StringField('Competition ID (the same one that is used on the WCA website):', validators = [Required()])
    compInfo = StringField('Competition Info:', validators = [Required()])
    event = SelectField("Select the event you want to see a psych sheet for", choices = [
      ("222"   , "2x2 Cube"),
      ("333"   , "Rubik's Cube"),
      ("333oh" , "Rubik's Cube: One-Handed"),
      ("333bf" , "Rubik's Cube: Blindfolded"),
      ("333fm" , "Rubik's Cube: Fewest moves"),
      ("333ft" , "Rubik's Cube: With feet"),
      ("333mbf", "Rubik's Cube: Multiple Blindfolded"),
      ("444"   , "4x4 Cube"),
      ("444bf" , "4x4 Cube: Blindfolded"),
      ("555"   , "5x5 Cube"),
      ("555bf" , "5x5 Cube: Blindfolded"),
      ("666"   , "6x6 Cube"),
      ("777"   , "7x7 Cube"),
      ("clock" , "Rubik's Clock"),
      ("minx"  , "Megaminx"),
      ("pyram" , "Pyraminx"),
      ("skewb" , "Skewb"),
      ("sq1"   , "Square-1")], validators = [Required()])
    submit = SubmitField('Submit')

#################################################################################
# Helper functions
# def createDataStructure(data):
#     compName = data['shortName']
#     people = data['persons']
#     compEvents = data['events']
def addScoreSheet(updatedScoreSheetTable, compName, eventName, roundNum, name, cutoff, timeLimit):
    updatedScoreSheetTable = updatedScoreSheetTable.replace("competitionName", compName
                                                  ).replace("eventName", eventName
                                                  ).replace("roundNumber", roundNum
                                                  ).replace("cutoffTime", cutoff
                                                  ).replace("timeLimit", timeLimit
                                                  ).replace("competitorName", name)
    return updatedScoreSheetTable

def makeScoreSheets(compName, roundNum, event, names, cutoff, timeLimit):
    '''
    Creates string with HTML that contains all of the necessary
    score sheets for the first round of the competition
    '''
    scoreSheetList = []
    updatedScoreSheetTable = ao5Table
    for num, person in enumerate(names.split(',')):
        scoreSheetList.append(addScoreSheet(updatedScoreSheetTable, compName, event, roundNum, person, cutoff, timeLimit))


    scoreSheets = str.join("\n", scoreSheetList)

    return startHTML + scoreSheets + endHTML


###############################################################################
## Routes and view functions

@app.route('/')
def home():
  return render_template("index.html")

@app.route('/scorecards', methods = ['GET', 'POST'])
def scorecards():
    form = RegistrationForm()
    if form.validate_on_submit() and request.method == 'POST':
        data = makeScoreSheets(request.form.get('compName'), request.form.get('roundNum'), request.form.get('event'), request.form.get('names'), request.form.get('cutoff'), request.form.get('timeLimit'))
        return render_template('view_heats.html', data=data)
    return render_template('scorecards.html', form=form)

@app.route('/wcif', methods = ['GET', 'POST'])
def wcif():
  wcif_form = WCIFInputForm()
  print(wcif_form.validate_on_submit())
  print(request.method)
  if request.method == 'POST':
    data = json.loads(request.form.get('compInfo'))
    info = []
    for person in data["persons"]:
      if "personalBests" in person:
        for event in person["personalBests"]:
          if event["eventId"] == request.form.get("event") and event["type"] == "average":
            info.append((int(event["best"]) / 100, person["name"]))
    info.sort()
    return render_template("psych_sheet.html", info=info)
  return render_template("wcif.html", form=wcif_form)



if __name__ == '__main__':
    # app.run(host = '0.0.0.0', port = int(os.getenv('PORT', 5001)))
    app.run()
