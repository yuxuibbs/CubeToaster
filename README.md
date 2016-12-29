# CubeToaster
Generates groups (heats) for WCA competitions to save time for organizers.

Outputs score sheets sorted by group number and event and a txt file with everyone's heat numbers.

1. Run heatsGenerator.py
2. Double check the information (especially competitor ID)
3. Print stuff
4. Cut the score sheets in order

Project started out as project 4 for SI 206 (was due on 12/02/2016).

Now taking pull requests.


## Heats
Generates groups based on JSON input (currently works for CubingUSA only)


**Instructions for organizers using the javascript version:**

1. Download the code from this repository, unzip if necessary, and run heatGenerator.html in your Browser.

2. Download the JSON file from cubingUSA (https://www.cubingusa.com/CompetitionName/admin/json.php) or use Anonymizer/fake.json for testing

3. Open the file in your preferred text editor, and copy all content

4. Paste the content into the big textarea

5. Fill in the number of timing stations and press "Continue"

6. Adjust the number of groups, then click generate

7. You will see all scoresheets.

8. Print to file (save as PDF) with 4 sheets per page

9. Print score sheets and cut them (everything is already sorted by event and group number)


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

## Anonymizer
Anonymizes JSON data for development purposes

## List of competition CubeToaster has been used in:
* Shaker Fall 2016

Future competitions:
* Dayton Winter 2017
* MCC Alpha 2017


The Javascript-Version was created by YTCuber.
