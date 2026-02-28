import pandas as pd

FILE_20_21 = "csv/laliga20-21.csv"
FILE_21_22 = "csv/laliga21-22.csv"
FILE_22_23 = "csv/laliga22-23.csv"
FILE_23_24 = "csv/laliga23-24.csv"
FILE_24_25 = "csv/laliga24-25.csv"

df_2020 = pd.read_csv(FILE_20_21,sep=",")
df_2021 = pd.read_csv(FILE_21_22,sep=",")
df_2022 = pd.read_csv(FILE_22_23,sep=",")
df_2023 = pd.read_csv(FILE_23_24,sep=",")
df_2024 = pd.read_csv(FILE_24_25,sep=",")

df_all = pd.concat([df_2020,df_2021,df_2022,df_2023,df_2024])

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

df_all = clean_dataset(df_all)

print(df_all.head(10))
print(len(df_all))
print(df_all.columns)