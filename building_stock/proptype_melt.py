import pandas as pd
import numpy as np

file_type = 'https://raw.githubusercontent.com/LondonEnergyMap/rawdata/master/building_stock/dwelling-property-type-2015-lsoa-msoa.csv'

dftype = pd.read_csv(file_type)

# select LSOA entries only
dftype_lsoa = dftype[dftype['GEOGRAPHY'].str.contains('LSOA')]

# drop Geography column as no longer needed
dftype_lsoa = dftype_lsoa.drop(columns='GEOGRAPHY')

# restructure the dataframe by melting the columns
# containing property type information to rows

typecols = dftype_lsoa.columns
df = pd.melt(dftype_lsoa, id_vars=typecols[0:3], value_vars=typecols[4:36],
             var_name='prop_type', value_name='ndwellings')

# drop rows which contains 'all' property types
droprows = ['BUNGALOW',
            'FLAT_MAIS',
            'HOUSE_TERRACED',
            'HOUSE_SEMI',
            'HOUSE_DETACHED',
            'ALL_PROPERTIES']
df = df[(~df.prop_type.isin(droprows))]

# extract number of bedroom from entry
df['nbeds'] = df.prop_type.str.extract('(\d+)')

# convert column to lower case
df['prop_type'] = df.prop_type.str.lower()

# split information of property type and form into 2 columns
types = ['bungalow', 'house', 'flat']
forms = ['terraced', 'semi', 'detached']

df['prop'] = df.prop_type
df['form'] = 'default'

for i in range(3):
    df['prop'] = np.where(df.prop_type.str.contains(types[i]), types[i], df.prop_type)
    df['form'] = np.where(df.prop_type.str.contains(forms[i]), forms[i], df.form)


df.drop(columns=['prop_type'], inplace=True)
df.columns = df.columns.str.lower()

# drop entries with 'ALL' council tax band
# df = df[(~df.band.str.contains('All'))]

# keep only entries with 'ALL' council tax band + drop column
df = df[(df.band.str.contains('All'))]
df.drop(columns=['band'], inplace=True)

# df.to_csv('proptype_lsoa.csv', index=False)
