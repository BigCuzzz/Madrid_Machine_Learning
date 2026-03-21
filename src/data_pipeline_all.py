#TO BE IMPLEMENTED

import pandas as pd

FILE_10_11 = "csv/laliga10-11.csv"
FILE_11_12 = "csv/laliga11-12.csv"
FILE_12_13 = "csv/laliga12-13.csv"
FILE_13_14 = "csv/laliga13-14.csv"
FILE_14_15 = "csv/laliga14-15.csv"
FILE_15_16 = "csv/laliga15-16.csv"
FILE_16_17 = "csv/laliga16-17.csv"
FILE_17_18 = "csv/laliga17-18.csv"
FILE_18_19 = "csv/laliga18-19.csv"
FILE_19_20 = "csv/laliga19-20.csv"
FILE_20_21 = "csv/laliga20-21.csv"
FILE_21_22 = "csv/laliga21-22.csv"
FILE_22_23 = "csv/laliga22-23.csv"
FILE_23_24 = "csv/laliga23-24.csv"
FILE_24_25 = "csv/laliga24-25.csv"


def clean_dataset(df):
    columns_to_drop = [
        'AvgC<2.5', 'AHCh', 'B365CAHH', 'B365CAHA', 'PCAHH', 'PCAHA', 'MaxCAHH',
        'MaxCAHA', 'AvgCAHH', 'AvgCAHA','B365H', 'B365D', 'B365A', 'BWH', 'BWD', 'BWA',
        'IWH', 'IWD', 'IWA', 'PSH', 'PSD', 'PSA', 'WHH', 'WHD', 'WHA', 'VCH',
        'VCD', 'VCA', 'MaxH', 'MaxD', 'MaxA', 'AvgH', 'AvgD', 'AvgA',
        'B365>2.5', 'B365<2.5', 'P>2.5', 'P<2.5', 'Max>2.5', 'Max<2.5',
        'Avg>2.5', 'Avg<2.5', 'AHh', 'B365AHH', 'B365AHA', 'PAHH', 'PAHA',
        'MaxAHH', 'MaxAHA', 'AvgAHH', 'AvgAHA', 'B365CH', 'B365CD', 'B365CA',
        'BWCH', 'BWCD', 'BWCA', 'IWCH', 'IWCD', 'IWCA', 'PSCH', 'PSCD', 'PSCA',
        'WHCH', 'WHCD', 'WHCA', 'VCCH', 'VCCD', 'VCCA', 'MaxCH', 'MaxCD',
        'MaxCA', 'AvgCH', 'AvgCD', 'AvgCA', 'B365C>2.5', 'B365C<2.5', 'PC>2.5',
        'PC<2.5', 'MaxC>2.5', 'MaxC<2.5', 'AvgC>2.5','BFH', 'BFD', 'BFA', '1XBH', 
        '1XBD', '1XBA', 'BFEH', 'BFED', 'BFEA', 'BFE>2.5', 'BFE<2.5', 'BFEAHH', 'BFEAHA',
        'BFCH', 'BFCD', 'BFCA', '1XBCH', '1XBCD', '1XBCA', 'BFECH', 'BFECD',
        'BFECA', 'BFEC>2.5', 'BFEC<2.5', 'BFECAHH', 'BFECAHA',"HTHG","HTR","HTAG"
                       ]
    df = df.drop(columns=columns_to_drop)
    return df

def load_raw_laliga():
    df_2010 = pd.read_csv(FILE_10_11,sep=",")
    df_2011 = pd.read_csv(FILE_11_12,sep=",")
    df_2012 = pd.read_csv(FILE_12_13,sep=",")
    df_2013 = pd.read_csv(FILE_13_14,sep=",")
    df_2014 = pd.read_csv(FILE_14_15,sep=",")
    df_2015 = pd.read_csv(FILE_15_16,sep=",")
    df_2016 = pd.read_csv(FILE_16_17,sep=",")
    df_2017 = pd.read_csv(FILE_17_18,sep=",")
    df_2018 = pd.read_csv(FILE_18_19,sep=",")
    df_2019 = pd.read_csv(FILE_19_20,sep=",")
    df_2020 = pd.read_csv(FILE_20_21,sep=",")
    df_2021 = pd.read_csv(FILE_21_22,sep=",")
    df_2022 = pd.read_csv(FILE_22_23,sep=",")
    df_2023 = pd.read_csv(FILE_23_24,sep=",")
    df_2024 = pd.read_csv(FILE_24_25,sep=",")

    df = pd.concat([df_2010,df_2011,df_2012,df_2013,df_2014,df_2015,df_2016,df_2017,df_2018,df_2019,df_2020,df_2021,df_2022,df_2023,df_2024])
    return df

def print_info(df):
    print(df.head(10))
    print(len(df))
    print(df.columns)

def build_df(df):
    df = clean_dataset(df)
    df = Convert_to_homeaway(df)
    df = convert_res_to_points(df)
    df = form_last5_games(df)
    df = drop_changed_columns(df)
    return df

if __name__ == "__main__":
    df_raw = load_raw_laliga()
    df = build_df(df_raw)
    print_info(df)
    df.to_parquet("csv/processed/all_matches.parquet", index=False)