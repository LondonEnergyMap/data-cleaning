import pandas as pd

filename = 'certificates.csv'

df = pd.read_csv(filename)


d = {'old': df.columns}
df_dict = pd.DataFrame(data=d)
df_dict.set_index('old', inplace=True)
df_dict['new']=[
        'key',
        'add1',
        'add2',
        'add3',
        'pcode',
        'bref',
        'current_opr',
        'yr1_opr',
        'yr2_op2',
        'oprband',
        'elecco2',
        'heatco2',
        'renewco2',
        'prop_type',
        'insp_date',
        'localauth_code',
        'constit_code',
        'county',
        'lodge_date',
        'benchmark',
        'mainheatingfuel',
        'otherfuel',
        'special',
        'renewables',
        'tfa',
        'annual_thermalfuel',
        'typ_thermalfuel',
        'annual_elec',
        'typ_elec',
        'renew_thermalfuel',
        'renew_elec',
        'yr1_elecco2',
        'yr2_elecco2',
        'yr1_heatingco2',
        'yr2_heatingco2',
        'yr1_renewco2',
        'yr2_renewco2',
        'ac',
        'ac_kw',
        'ac_estimate',
        'ac_insp',
        'modes',
        'category',
        'addfull',
        'localauth',
        'constit',
        'certificate'
        ]

# convert dataframe to dictionary
col_dict = df_dict['new'].to_dict()
df.rename(columns = col_dict, inplace=True)

# drop columns that are co2 parameters
keepcols=[
        'key',
        'add1',
        'add2',
        'add3',
        'pcode',
        'bref',
        'prop_type',
        'insp_date',
        'localauth_code',
        'constit_code',
        'county',
        'lodge_date',
        'benchmark',
        'mainheatingfuel',
        'otherfuel',
        'special',
        'renewables',
        'tfa',
        'annual_thermalfuel',
        'typ_thermalfuel',
        'annual_elec',
        'typ_elec',
        'renew_thermalfuel',
        'renew_elec',
        'ac',
        'ac_kw',
        'ac_estimate',
        'ac_insp',
        'modes',
        'category',
        'addfull',
        'localauth',
        'constit',
        'certificate'
        ]

df = df[keepcols]

# convert columns to datetime format
df['insp_date']= pd.to_datetime(df.insp_date, format='%Y-%m-%d')
print(df.insp_date.head())
