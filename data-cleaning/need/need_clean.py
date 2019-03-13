# set up libraries and packages
import pandas as pd

# read csv file from github repository (so that filepath remains unchanged on any computer or folder, and there is no need to download)
filepath = 'https://raw.githubusercontent.com/LondonEnergyMap/rawdata/master/need/need_public_use_file_2014.csv'

# read csv into dataframe
df = pd.read_csv(filepath)

# keep only London region entries
london = 'E12000007'
df = df[df.REGION==london]

# drop columns "REGION, IMD_WALES
df = df.drop(columns=['REGION', 'IMD_WALES'])

# --------
# restructure dataframe so that gas and electricity columns are expressed in separate columns with a year column, instead of expressed as a single consumption in year column

# select all the headings containing 'gcons' (but not validation columns)
colheads = df.columns
gcons = [c for c in colheads if ('Gcons' in c) & ('Valid' not in c)]

# use the remaining columns (except validation columns) as identifier
colheads_gaskeep = [x for x in colheads if ('Gcons' not in x) & ('Valid' not in x)]

# set lower and upper limits for gas consumption (NEED uses 100, 50000, sub-national statistics use 73,000)
gas_lowerlim = 100
gas_upperlim = 50000

# 'melt' the dataframe so some columns become row entries with column header as new column
df1 = pd.melt(df, id_vars=colheads_gaskeep, value_vars=gcons, var_name='col_name', value_name='gcons')

# drop entries outside of gas consumption limits
df1 = df1[(df1.gcons.notnull()) | ((df1.gcons > gas_lowerlim) & (df1.gcons<gas_upperlim))]

# keep only year part of col_name and save as new column
df1['year'] = df1.col_name.astype(str).str[5:9]
df1 = df1.drop(columns='col_name')

# repeat restructure for electricity consumption columns
econs = [c for c in colheads if ('Econs' in c) & ('Valid' not in c)]
df_econs = pd.melt(df1, id_vars='HH_ID', value_vars=econs, var_name='col_name', value_name='econs')
elec_lowerlim = 100
elec_upperlim = 25000
df_econs = df_econs[(df_econs.econs.notnull()) | ((df_econs.econs>elec_lowerlim) & (df_econs.econs<elec_upperlim))]
df_econs['year'] = df_econs.col_name.astype(str).str[5:9]
df_econs = df_econs.drop(columns='col_name')

# drop econs columns in gas consumption dataframe then merge on house id (HHID) and year
df1 = df1.drop(columns=econs)
ldn = df1.merge(df_econs, how='inner', left_on=['HH_ID', 'year'], right_on=['HH_ID', 'year'])
ldn.drop_duplicates(inplace=True)
ldn = ldn.sort_values(by='HH_ID')
ldn = ldn.reset_index(drop=True)

# convert year column from object to int
ldn['year'] = pd.to_numeric(ldn.year)

# -----------

# make column headers into dictionary to rename by creating dataframe of old column headers and new column headers and then convert to dictionary
coldf = {'old': ldn.columns}
df_dict = pd.DataFrame(data=coldf)
df_dict.set_index('old', inplace=True)

df_dict['new'] = ['hid',
    'imd_eng',
    'e7',
    'mainheatfuel',
    'age',
    'proptype',
    'floorarea_band',
    'epc_band',
    'loftdepth',
    'walls',
    'cwi',
    'cwi_year',
    'loftins',
    'loftins_year',
    'boiler',
    'boiler_year',
    'gcons',
    'year',
    'econs'
]

col_dict = df_dict['new'].to_dict()

# rename column headers using column dictionary (col_dict)
ldn.rename(columns = col_dict, inplace=True)

# export cleaned dataframe to csv
ldn.to_csv('need_ldn.csv')
