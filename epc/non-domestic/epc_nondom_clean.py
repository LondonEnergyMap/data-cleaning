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
    path_start = 'https://raw.githubusercontent.com/LondonEnergyMap/rawdata/master/epc/nondomestic_epc_london/non-domestic-'
    path_end = '/certificates.csv'

    # start by loading the first borough into dataframe df, by making a full filepath using filename of the borough
    filename = boroughs[0]
    filepath = path_start + filename + path_end
    df = pd.read_csv(filepath)
    
    # rename column headers using function defined at end of script
    df, df_dict = rename_epcnondom(df)

    # keep only entries of the latest date (to keep dataframe size small) by converting inspection date column to datetime format and dropping duplicate entries based on building reference and address, and keeping only last ascending date entry
    df['insp_date']= pd.to_datetime(df['insp_date'], format='%Y-%m-%d')
    df = df.sort_values(by='insp_date').drop_duplicates(['add2', 'bref'], keep='last')

    # repeat the whole process of loading csv to dataframe by going through whole list of london boroughs filenames, whilst keeping latest date entry, and then append each dataframe to the last one
    for i in range(1,nboroughs):
        tempname = boroughs[i]
        tempath = path_start + tempname + path_end
        temp = pd.read_csv(tempath)

        temp, temp_dict  = rename_epcnondom(temp)


        temp['insp_date']= pd.to_datetime(temp['insp_date'], format='%Y-%m-%d')
        temp = temp.sort_values(by='insp_date').drop_duplicates(['add2', 'bref'], keep='last')
        df = pd.concat([df, temp])
    
    # ---------------------


    df.to_csv('epc_nondomestic_ldn.csv')

#---------------------------

def rename_epcnondom(df):
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
            'assetr', 
            'assetr_band',       
            'prop_type', 
            'insp_date', 
            'localauth_code', 
            'constit_code',
            'county', 
            'lodge_date', 
            'transact_type', 
            'newb_benchmark',
            'exb_benchmark', 
            'complexity', 
            'mainheatingfuel',
            'otherfuel', 
            'special', 
            'renewables',  
            'tfa', 
            'co2', 
            'co2_target',
            'co2_typical', 
            'co2_building',
            'ac',
            'ac_kw',
            'ac_estimate',
            'ac_insp',
            'modes',
            'addfull',
            'localauth',
            'constit',
            'certificate'
            ]

    # convert dataframe to dictionary
    col_dict = df_dict['new'].to_dict()
    df.rename(columns = col_dict, inplace=True)
    
    return df, df_dict

#---------------------------

if __name__=="__main__":
    main()

