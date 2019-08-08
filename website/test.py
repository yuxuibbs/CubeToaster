import pandas as pd
import numpy as np
import jellyfish

def create_heats(df, event, num_heats):
    counter = 0
    for row_num, registration_status in enumerate(df[event]):
        if registration_status != '0':
            df.loc[row_num, event] = counter % num_heats + 1
            counter += 1


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

comp_events = []

df = pd.read_csv(input_file, dtype=str, sep=',').drop(['Status', 'Country', 'Birth Date', 'Gender', 'Email', 'Guests', 'IP'], axis=1)


# df = df.replace('0', np.NaN)
df['staff'] = 0

for event in allEventsDict:
    if event in df:
        comp_events.append(event)
        create_heats(df, event, num_heats[event])

df['FirstName'] = (df['Name'].str.split(expand=True)[0])
df['MRA'] = df['FirstName'].apply(jellyfish.match_rating_codex)

print(df.head(50))

for event in comp_events:
    grouped_df = df.groupby(event)
    for key, item in grouped_df:
        if key != '0':
            print(key)
            print(grouped_df.get_group(key)[['Name', event, 'MRA']].sort_values(by='MRA'))
            print()
            print()

df.to_csv('test.csv')