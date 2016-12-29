# CubeToaster
Generates groups (heats) for WCA competitions to save time for organizers.

Outputs score sheets sorted by group number and event and a txt file with everyone's heat numbers.

1. Run heatsGenerator.py
2. Double check the information (especially competitor ID)
3. Print stuff
4. Cut the score sheets in order

Project started out as project 4 for SI 206 (was due on 12/02/2016).

Now taking pull requests.


## Website version
(Available at here)[https://yuxuibbs.github.io/CubeToaster/Javascript/heatGenerator.html]

Issues:

* Competitor ID does not match cubecomps competitor ID

* Currently does not generate a page with information on competitor's assigned groups


## Heats
Generates groups based on JSON input (currently works for CubingUSA only)

**Instructions for organizers using the python version:**

1. Download the code from this repository

2. Download the JSON file from cubingUSA (https://www.cubingusa.com/CompetitionName/admin/json.php)

3. Place the JSON file in the same folder as the rest of the code (inside the Heats folder)

4. Run heatGenerator.py

5. Enter prompts as necessary (might have to edit two files)

6. Make sure screen.css is in the same folder as scoresheets.html

7. Open scoresheets.html

8. Print to file (save as PDF) with 4 sheets per page

9. Print score sheets and cut them (everything is already sorted by event and group number)


**Issues:**

* Competitor ID might be wrong (fails when more than 1 person has the same name)


## Anonymizer
Anonymizes JSON data for development purposes


## List of competition CubeToaster has been used in:
* Shaker Fall 2016

Future competitions:
* Dayton Winter 2017
* MCC Alpha 2017
