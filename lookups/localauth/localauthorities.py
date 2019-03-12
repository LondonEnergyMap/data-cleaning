import pandas as pd


filename = 'localauthority_lookup.csv'
df = pd.read_csv(filename)
df['london'] = 0

# define local authorities in London
london = [
        'City of London',
        'Westminster', 
        'Kensington and Chelsea',
        'Hammersmith and Fulham',
        'Wandsworth',
        'Lambeth',
        'Southwark',
        'Tower Hamlets',
        'Hackney',
        'Islington',
        'Camden',
        'Brent',
        'Ealing',
        'Hounslow',
        'Richmond',
        'Kingston',
        'Merton',
        'Sutton',
        'Croydon',
        'Bromley',
        'Lewisham',
        'Greenwich',
        'Bexley',
        'Havering',
        'Barking and Dagenham',
        'Redbridge',
        'Newham',
        'Waltham Forest',
        'Haringey',
        'Enfield',
        'Barnet',
        'Harrow',
        'Hillingdon'
        ]

# rename columns in order
df.columns = ['code', 'localauthority', 'fid', 'london']

# select the local authorities in London and change value of 'london' column to 1
df.loc[df.localauthority.isin(london), ['london']] = 1

print(df.loc[df.london==1])

# write to csv
df.to_csv('localauthority_lookuptable.csv')
