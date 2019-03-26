import pandas as pd

gasfile = 'http://raw.githubusercontent.com/LondonEnergyMap/rawdata/master/consumption_postcode/gas/Postcode_level_gas_estimates_2015_experimental.csv'

elecfile = 'http://raw.githubusercontent.com/LondonEnergyMap/rawdata/master/consumption_postcode/electricity/Postcode_level_electricity_estimates_2015_experimental.csv'

# ------------
# select london only postcodes
# ------------


def ldn_pcode(file):
    # read input file
    df_all = pd.read_csv(file)

    # drop dubplicates
    df_all = df_all.drop_duplicates()

    # make a copy of the dataframe
    df1 = df_all.copy()

    # make a column containing first letter of the postcode only
    df1['firstletter'] = df_all['POSTCODE'].str[0]

    # select rows which the first letter is N, E, S, W only
    df1 = df1[
        (df1.firstletter.str.startswith('N')) |
        (df1.firstletter.str.startswith('E')) |
        (df1.firstletter.str.startswith('S')) |
        (df1.firstletter.str.match('W'))]

    # drop the column containing first letter only as we no long need it
    df1.drop(columns='firstletter', inplace=True)

    # make df2 which selects all london postcodes defined by first 2 letters
    df2 = df_all[
        (df_all['POSTCODE'].str[0:2].str.startswith('NW')) |
        (df_all['POSTCODE'].str[0:2].str.startswith('SE')) |
        (df_all['POSTCODE'].str[0:2].str.startswith('SW')) |
        (df_all['POSTCODE'].str[0:2].str.startswith('EC')) |
        (df_all['POSTCODE'].str[0:2].str.startswith('WC')) |
        (df_all['POSTCODE'].str[0:2].str.startswith('WD')) |
        (df_all['POSTCODE'].str[0:2].str.startswith('EN')) |
        (df_all['POSTCODE'].str[0:2].str.startswith('HA')) |
        (df_all['POSTCODE'].str[0:2].str.startswith('IG')) |
        (df_all['POSTCODE'].str[0:2].str.startswith('UB')) |
        (df_all['POSTCODE'].str[0:2].str.startswith('TW')) |
        (df_all['POSTCODE'].str[0:2].str.startswith('KT')) |
        (df_all['POSTCODE'].str[0:2].str.startswith('SM')) |
        (df_all['POSTCODE'].str[0:2].str.startswith('CR')) |
        (df_all['POSTCODE'].str[0:2].str.startswith('BR')) |
        (df_all['POSTCODE'].str[0:2].str.startswith('DA')) |
        (df_all['POSTCODE'].str[0:2].str.startswith('RM'))]

    # append the 2 dataframes into 1
    df = df1.append(df2, ignore_index=True)

    # rename columns
    df.columns = ['pcode', 'cons', 'nmeter', 'avg', 'mid']

    return df


# create gas and electricity london only postcode estimates
dfgas = ldn_pcode(gasfile)
dfgas.to_csv('gascons_pcodeldn.csv')

dfelec = ldn_pcode(elecfile)
dfelec.to_csv('eleccons_pcodeldn.csv')
