# CubeToaster
Generates heats for WCA competitions to save time for organizers.

Outputs score sheets sorted by heat number and event and a txt file with everyone's heat numbers. 

1. Run heatsGenerator.py
2. Double check the information
3. Print stuff (score sheets and heat sheets)
4. Cut the score sheets in order
????
5. Profit (save at least 4 hours of figuring out heats and sorting score sheets) 

Project started out as project 4 for SI 206 (was due on 12/02/2016). 

Now taking pull requests.


## Heats
Generates heats based on JSON input (currently works for CubingUSA)

Instructions for organizers:

1. Download the code from this repository

2. Download the JSON file from cubingUSA (https://www.cubingusa.com/CompetitionName/admin/json.php)

3. Place the JSON file in the same folder as the rest of the code (inside the Heats folder)

4. Run heatGenerator.py

5. Enter prompts as necessary (might have to edit two files)

6. Make sure screen.css is in the same folder as scoresheets.html

7. Open scoresheets.html

8. Print to file (save as PDF) with 4 sheets per page

9. Print score sheets and cut them (everything is already sorted by event and heat number)


### Heat Generator


## Anonymizer
Anonymizes JSON data