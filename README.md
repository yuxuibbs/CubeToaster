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

Score sheets and name tags are dependant on group generation so make sure to do everything in the generating groups section first.

[Generating groups]

1. Download the code from this repository

2. Download the JSON file from cubingUSA (https://www.cubingusa.com/CompetitionName/admin/json.php) replace CompetitionName with the competition name

3. Place the JSON file in the same folder as the rest of the code (inside the Heats folder)

4. Run heatGenerator.py

5. Follow the prompts as necessary

6. Print printableGroups.txt to give to competitors

7. Double check and print printableGroups.csv to post on walls

[Making score sheets]

1. Run sheetGenerator.py

2. Make sure screen.css is in the same folder as scoresheets.html

3. Open scoresheets.html (Chrome or Firefox is preferred; might not work on Internet Explorer)

4. Print to file (save as PDF) with 4 sheets per page

5. Print score sheets (make sure it is 4 per page)

6. Cut score sheets (everything is already sorted by event and group number)

[Making name tags]

1. Run generateNameTags.py to get name tags (might have to mess with the CSS)

2. Open nameTags.html

3. Make sure everything lines up properly

4. Print nameTags.html


**Issues:**

* Competitor ID might be wrong (fails when more than 1 person has the same name)
* There is a chance staff and a non-staff competitor with the same name will be in the same group


## Anonymizer
Anonymizes JSON data for development purposes
