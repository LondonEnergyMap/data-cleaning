import pandas as pd

gasfile = 'http://raw.githubusercontent.com/LondonEnergyMap/cleandata/master/consumption_postcode/gascons_pcodeldn.csv'
elecfile = 'http://raw.githubusercontent.com/LondonEnergyMap/cleandata/master/consumption_postcode/eleccons_pcodeldn.csv'

dfgas = pd.read_csv(gasfile)
dfgas.columns = ['pcgas', 'gascons', 'gasmeters', 'gasavg', 'gasmid']

dfelec = pd.read_csv(elecfile)
dfelec.columns = ['pcelec', 'eleccons', 'elecmeters', 'elecavg', 'elecmid']

epcfile = 'https://media.githubusercontent.com/media/LondonEnergyMap/cleandata/master/epc/domestic/epc_domestic_ldn.csv'
# epcfile = 'http://raw.githubusercontent.com/LondonEnergyMap/cleandata/master/epc/domestic/epcdom_sample.csv'
dfepc = pd.read_csv(epcfile)
dfepc = dfepc.drop(dfepc.columns[0], axis=1)

# drop the following columns not useful for analysis
dropcols = [
        'curr_eff',
        'poten_eff',
        'county',
        'lodge_date',
        'curr_envirr',
        'poten_envirr',
        'curr_light',
        'poten_light',
        'curr_heatcost',
        'poten_heatcost',
        'curr_hotwtr',
        'poten_hotwtr',
        'tariff',
        'hotwtr_enveff',
        'floor_enveff',
        'window_enveff',
        'wall_enveff',
        'heat2_enveff',
        'roof_enveff',
        'heat_enveff',
        'control_enveff',
        'light_enveff',
        'corridor',
        'unhcorridor',
        'addfull',
        'localauth',
        'constit',
        'certificateh'
        ]
dfepc = dfepc.drop(dropcols, axis=1)


def merge_pcode(dfepc, dfpc, match):

    # merge entries with exact postcode match
    df = dfepc.merge(
        dfpc, how='inner', left_on=['pcode'], right_on=dfpc.columns[0])

    # add column to indicate the entries are exact postcode matches
    df[match] = 'exact'

    # match the remaining entries that did not have exact postcode matches to
    # partial match
    dfremain = dfepc.copy()
    dfremain = dfremain[(~dfremain.pcode.isin(df.pcode))]

    # split the postcode into 2 parts and match only first part
    pc = dfremain.pcode.str.split(' ', n=1, expand=True)
    dfremain['pc1'] = pc[0]
    dfremain['pc2'] = pc[1]

    # drop postcode entries that do not have full postcodes
    pctemp = dfpc.columns[0]
    dfpcshort = dfpc[dfpc[pctemp].str.len() <= 3]

    # merge the remaining epc dataframe with partial postcodes
    dftemp = dfremain.merge(
        dfpcshort, how='inner', left_on=['pc1'], right_on=dfpcshort.columns[0])

    # add column to indicate the entries will be partial matches
    dftemp[match] = 'partial'

    # append the partical postcode match to full postcode match dataframe after
    # dropping additional columns
    dftemp = dftemp.drop(columns=['pc1', 'pc2'])
    df = df.append(dftemp)

    # add tag to the leftover entries that do not match any postcodes and
    # append back to main dataframe
    dfleftover = dfepc.copy()
    dfleftover = dfleftover[(~dfleftover.pcode.isin(df.pcode))]

    # fill empty columns with Nan in order to append to main dataframe
    for i in range(len(dfpc.columns)):
        dfleftover[dfpc.columns[i]] = 'Nan'

    dfleftover[match] = 'nomatch'
    df = df.append(dfleftover)

    # drop the repeated postcode column
    df = df.drop(dfpc.columns[0], axis=1)

    return df


# merge postcode gas consumptions to epc dataframe
df = merge_pcode(dfepc, dfgas, 'gasmatch')

# merge postcode electricity consumption to previous dataframe
df = merge_pcode(df, dfelec, 'elecmatch')

# write output to csv
df.to_csv('epc_postcodefull.csv', index=False)
# df.to_csv('epc_postcodesample.csv', index=False)
