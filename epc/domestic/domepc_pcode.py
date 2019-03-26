import pandas as pd

gasfile = 'http://raw.githubusercontent.com/LondonEnergyMap/cleandata/master/gascons_pcodeldn.csv'
elecfile = 'http://raw.githubusercontent.com/LondonEnergyMap/cleandata/master/eleccons_pcodeldn.csv'

epcfile = 'http://raw.githubusercontent.com/LondonEnergyMap/cleandata/master/epcdom_sample.csv'

dfepc = pd.read_csv(epcfile)


dfgas = pd.read_csv(gasfile)
dfgas = dfgas.drop(dfgas.columns[0], axis='columns')
print(dfgas.columns)
dfgas.columns = ['pcgas', 'gascons', 'gasmeters', 'gasavg', 'gasmid']

print(dfgas.shape)
print(dfgas.pcgas.unique())

dfgas.drop_duplicates(inplace=True)
print(dfgas.shape)

# dfelec = pd.read_csv(elecfile)
# dfelec.columns = ['eleccons', 'elecmeters', 'elecavg', 'elecmid']

# start with gas (but turn into function)

# # merge entries with exact postcode match
# df = dfepc.merge(dfgas, how='inner', left_on=['pcode'], right_on=['pcgas'])

# print(df.shape)

# df.drop_duplicates(inplace=True)
# print(df.shape)

# df.drop_duplicates(subset=['pcode', 'bref'], inplace=True)

# print(df.shape)
# print(df.columns)

# # if there are more than 1 match, merge creates duplicates so drop duplicate entries

# # 