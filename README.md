# CubeToaster
Generates groups (heats) for WCA competitions to save time for organizers.

Outputs score sheets sorted by group number and event and some files with everyone's heat numbers.

Project started out as project 4 for SI 206 (was due on 12/02/2016).

Now taking pull requests.


## Website version
Old version of CubeToaster is [available here](https://yuxuibbs.github.io/CubeToaster/Javascript/heatGenerator.html)

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

5. Follow the prompts as necessary

6. Run sheetGenerator.py

7. Make sure screen.css is in the same folder as scoresheets.html

8. Open scoresheets.html

9. Print to file (save as PDF) with 4 sheets per page

10. Print score sheets and cut them (everything is already sorted by event and group number)

11. (optional) run generateNameTags.py to get name tags (might have to mess with the CSS)


**Issues:**

* Competitor ID might be wrong (fails when more than 1 person has the same name)
* There is a chance staff and a non-staff competitor with the same name will be in the same group


## Anonymizer
Anonymizes JSON data for development purposes
