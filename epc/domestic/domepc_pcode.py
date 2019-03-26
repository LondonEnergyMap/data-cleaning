import pandas as pd

gasfile = 'http://raw.githubusercontent.com/LondonEnergyMap/cleandata/master/gascons_pcodeldn.csv'
elecfile = 'http://raw.githubusercontent.com/LondonEnergyMap/cleandata/master/eleccons_pcodeldn.csv'

epcfile = 'http://raw.githubusercontent.com/LondonEnergyMap/cleandata/master/epcdom_sample.csv'

dfepc = pd.read_csv(epcfile)

dfgas = pd.read_csv(gasfile)
dfelec = pd.read_csv(elecfile)


# merge entries with exact postcode match

# if there are more than 1 match, merge creates duplicates so drop duplicate entries

# 