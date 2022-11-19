import os
import re
from pathlib import Path
from hashlib import sha256
import pandas as pd
import numpy as np
import warnings

# some display settings
warnings.filterwarnings('ignore')
pd.options.display.max_rows = 100
pd.options.display.max_columns = 100

# set paths for input and output folders
# use posix path from pathlib to cater for different operating systems
current_folder = Path(__file__).resolve().parent
input_folder = current_folder / 'input'
successful_folder = current_folder / 'output' / 'successful'
unsuccessful_folder = current_folder / 'output' / 'unsuccessful'



def extract_data():
    """
    read all csv files from the input folder
    """

    input_files = [f for f in input_folder.iterdir() if f.suffix=='.csv']
    df = pd.concat([pd.read_csv(f) for f in input_files], axis=0, ignore_index=True)
    return df


def validate_data(df):
    """
    clean up input data columns, validate the inputs against the given criteria
    """

    # clean up mobile_no, check if it is of 8 digits
    df['mobile_no'] = df['mobile_no'].str.strip() \
                                     .str.replace(' ', '')

    mobile_pattern = r'[0-9]{8}'
    df['valid_mobile'] = [True if re.fullmatch(mobile_pattern, m) else False for m in df['mobile_no']]

    # clean up date_of_birth, add above_18 flag
    df['date_of_birth'] = np.where(df['date_of_birth'].str.contains('-'), pd.to_datetime(df['date_of_birth'], dayfirst=True, infer_datetime_format=True).dt.strftime('%Y%m%d'), \
                                    pd.to_datetime(df['date_of_birth'], infer_datetime_format=True).dt.strftime('%Y%m%d'))

    date_ref = pd.to_datetime('2022-01-01')
    df['above_18'] = ( (date_ref - pd.to_datetime(df['date_of_birth'])) / np.timedelta64(1, 'Y') ) > 18

    # check email addresses, .com or .net
    # not that email address is case insensitive
    email_pattern = r'\b[a-z0-9._-]+@[a-z0-9.-]+\.(?:com|net)\b'
    df['valid_email']  = [True if re.fullmatch(email_pattern, e, flags=re.IGNORECASE) else False for e in df['email'] ]

    # combining all criteria to generate success flag
    df['success'] = np.where( (~df['name'].isna()) & (df['name'].str.len()>1) & (df['valid_mobile']) & (df['above_18']) & (df['valid_email']) , True, False)


    # remove prefix / suffix in names and split into first / last names
    df['name_cleaned'] = df['name'].str.replace('|'.join(['^Mr. ', '^Mrs. ', '^Ms. ', '^Miss ', '^Dr. ', ' PhD$', ' MD$', ' DVM$', ' DDS$', ' Jr.$']), '', regex=True) \
                                                         .str.strip() 
    name_part = df['name_cleaned'].str.partition(' ') # use partition for easier handling of ValueError  
    df['first_name']  = name_part[0]
    df['last_name'] = name_part[2]
    
    return df

def transform_load(df):
    """
    create hash for successful applications
    output to 'successful' and 'unsuccessful' folders 
    """

    # split data in to successful / unsuccessful tables
    df_successful = df[df['success']]
    df_unsuccessful = df[~df['success']]
    
    # create membership ID as <last_name>_<hash(YYYYMMDD)>
    dob_hashed = df_successful['date_of_birth'].apply(lambda x: sha256(x.encode('utf-8')).hexdigest()[:5] )
    df_successful['membership_id'] = df_successful['last_name'] + dob_hashed
    
    # output processed data, remove columns not needed
    df_successful = df_successful[['membership_id', 'name', 'first_name', 'last_name', 'date_of_birth', 'mobile_no', 'email', 'above_18']]
    df_successful.to_csv(successful_folder / 'processed_successful.csv', index = False)

    df_unsuccessful = df_unsuccessful[['name', 'first_name', 'last_name', 'date_of_birth', 'mobile_no', 'email', 'above_18']]
    df_unsuccessful.to_csv(unsuccessful_folder / 'processed_unsuccessful.csv', index = False)

    return df_successful, df_unsuccessful





df = extract_data()
df = validate_data(df)
df_successful, df_unsuccessful = transform_load(df)

# print(df_successful.shape)
# print(df_successful.head(20))