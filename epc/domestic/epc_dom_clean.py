# set up libraries and packages
import pandas as pd

def main():
    # read london boroughs lookup table file from github repository (so that filepath remains unchanged on any computer or folder, and there is no need to download)
    boroughspath = 'https://raw.githubusercontent.com/LondonEnergyMap/rawdata/master/boroughsldn_lookup/localauthority_lookuptable.csv'

    # read file to dataframe, and keep only boroughs in London
    df_lookup = pd.read_csv(boroughspath)
    ldnboroughs_temp = df_lookup[df_lookup.london==1]
    ldnboroughs = ldnboroughs_temp.copy()
    nboroughs = len(ldnboroughs)

    # ------
    # create a list of filename that corresponds to how the epcs certificates are stored

    # replace borough column spaces with -
    ldnboroughs['la']=ldnboroughs.localauthority.replace(' ','-',regex=True)

    # make list of filenames from borough codes and names from lookup table
    boroughs = ldnboroughs.code + '-' + ldnboroughs.la
    boroughs.reset_index(drop=True, inplace=True)

    # ----------------
    # merge all the london boroughs epcs certificates into 1 file by iteratively go through all the london borough folders stored on github

    # define first and end parts of the file path that remain the same for each folder
    path_start = 'https://raw.githubusercontent.com/LondonEnergyMap/rawdata/master/epc/domestic_epc_london/domestic-'
    path_end = '/certificates.csv'

    # start by loading the first borough into dataframe df, by making a full filepath using filename of the borough
    filename = boroughs[0]
    filepath = path_start + filename + path_end
    df = pd.read_csv(filepath)
    
    # rename column headers using function defined at end of script
    df, df_dict = rename_epcdom(df)


    
    print(df.memory_usage(index=True).sum())

    # reduce dataframe size by changing types of columns using function defined at end of script
    df = changetypes(df, df_dict)


    print(df.memory_usage(index=True).sum())

    # keep only entries of the latest date (to keep dataframe size small) by converting inspection date column to datetime format and dropping duplicate entries based on building reference and address, and keeping only last ascending date entry
    df['insp_date']= pd.to_datetime(df['insp_date'], format='%Y-%m-%d')
    df = df.sort_values(by='insp_date').drop_duplicates(['add2', 'bref'], keep='last')

    # repeat the whole process of loading csv to dataframe by going through whole list of london boroughs filenames, whilst keeping latest date entry, and then append each dataframe to the last one
    for i in range(1,nboroughs):
        tempname = boroughs[i]
        tempath = path_start + tempname + path_end
        temp = pd.read_csv(tempath)

        temp, temp_dict  = rename_epcdom(temp)
        temp = changetypes(temp, temp_dict)

        temp['insp_date']= pd.to_datetime(temp['insp_date'], format='%Y-%m-%d')
        temp = temp.sort_values(by='insp_date').drop_duplicates(['add2', 'bref'], keep='last')
        df = pd.concat([df, temp])
        print(tempname)
        print(temp.shape)
        print(temp.head(2))
    # ---------------------


    print(df.shape)
    df.to_csv('epc_domestic_ldn.csv')


def changetypes(df, df_dict):
    # reduce dataframe size by changing column types
    # change to category
    cat = [6, 10, 11, 17, 32, 33, 34, 35, 39, 40, 47, 48, 50,51, 53,54, 56,57, 59,60, 62,63, 65,66, 68,69, 71,72, 75, 79, 80]
    for i in range(len(cat)):
        tempcol = df_dict.new[cat[i]]
        df[tempcol] = df[tempcol].astype('category')

    # change to float32
    floatlist = [22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 76, 77]
    for i in range(len(floatlist)):
        tempcol = df_dict.new[floatlist[i]]
        df[tempcol] = df[tempcol].astype('float32')

    # change to int32
    intlist = [8, 18, 19, 20, 21]
    for i in range(len(intlist)):
        tempcol = df_dict.new[intlist[i]]
        df[tempcol] = df[tempcol].astype('int32')

    # change from floating to int32
    f2int = [36, 38, 41, 42, 43, 44, 45, 74, 78] #winturbine(74) use -100?

    # cannot convert float to int if there are missing values, so first convert NaN to -1
    for i in range(len(f2int)):
        tempcol = df_dict.new[f2int[i]]
        df[tempcol].fillna(-1, inplace=True)
        df[tempcol] = df[tempcol].astype('int32')
    return df

def rename_epcdom(df):
    # rename column headers
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
            'curr_enr',
            'poten_enr',
            'curr_eff',
            'poten_eff',
            'prop_type',
            'builtform',
            'insp_date',
            'localauth_code',
            'constit_code',
            'county',
            'lodge_date',
            'transact_type',
            'curr_envirr',
            'poten_envirr',
            'curr_encons',
            'poten_encons',
            'curr_co2',
            'curr_co2perarea',
            'poten_co2',
            'curr_light',
            'poten_light',
            'curr_heatcost',
            'poten_heatcost',
            'curr_hotwtr',
            'poten_hotwtr',
            'tfa',
            'tariff',
            'mainsgas',
            'flvl',
            'flattop',
            'flattop_cnt',
            'mainheatcontrol',
            'glaze_percent',
            'glaze_type',
            'glaze_area',
            'nextension',
            'nrooms',
            'nheatedrooms',
            'led_percent',
            'nfireplace',
            'hotwtr',
            'hotwtr_eff',
            'hotwtr_enveff',
            'floor',
            'floor_eff',
            'floor_enveff',
            'window',
            'window_eff',
            'window_enveff',
            'wall',
            'wall_eff',
            'wall_enveff',
            'heat2',
            'heat2_eff',
            'heat2_enveff',
            'roof',
            'roof_eff',
            'roof_enveff',
            'heat',
            'heat_eff',
            'heat_enveff',
            'control',
            'control_eff',
            'control_enveff',
            'light',
            'light_eff',
            'light_enveff',
            'mainfuel',
            'windt',
            'corridor',
            'unhcorridor',
            'fheight',
            'pv',
            'solarwtr',
            'mechvent',
            'addfull',
            'localauth',
            'constit',
            'certificateh'
            ]

    # convert dataframe to dictionary
    col_dict = df_dict['new'].to_dict()
    df.rename(columns = col_dict, inplace=True)
    
    return df, df_dict

if __name__=="__main__":
    main()
