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

df = pd.concat([df_2020,df_2021,df_2022,df_2023,df_2024])

def madrid_filter(df):
    df = df[(df["HomeTeam"]=="Real Madrid") | (df["AwayTeam"]=="Real Madrid")]
    df = df.reset_index(drop=True)
    return df

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
        'WHCH', 'WHCD', 'WHCA', 'VCCH', 'VCCD', 'VCCA', 'MaxCH', 'MaxCD',"Div",
        'MaxCA', 'AvgCH', 'AvgCD', 'AvgCA', 'B365C>2.5', 'B365C<2.5', 'PC>2.5',
        'PC<2.5', 'MaxC>2.5', 'MaxC<2.5', 'AvgC>2.5','BFH', 'BFD', 'BFA', '1XBH', 
        '1XBD', '1XBA', 'BFEH', 'BFED', 'BFEA', 'BFE>2.5', 'BFE<2.5', 'BFEAHH', 'BFEAHA',
        'BFCH', 'BFCD', 'BFCA', '1XBCH', '1XBCD', '1XBCA', 'BFECH', 'BFECD',
        'BFECA', 'BFEC>2.5', 'BFEC<2.5', 'BFECAHH', 'BFECAHA',"HTHG","HTR","HTAG"
                       ]
    df = df.drop(columns=columns_to_drop)
    return df

def drop_changed_columns(df):
    columns_to_drop = [
        "FTHG","FTAG","HS","AS","HomeTeam","AwayTeam","HST","AST"
                       ]
    df = df.drop(columns=columns_to_drop)
    #Not processed yet
    columns_to_drop = ["HF","AF","HC","AC","HY","AY","HR","AR"]
    df = df.drop(columns=columns_to_drop)
    return df

def convert_res_to_points(df):
    #3 points for win, 1 for draw, 0 for loss
    is_home = df["HomeTeam"] == "Real Madrid"
    df["points"] = 0
    df.loc[is_home & (df["FTR"] == "H"), "points"] = 3
    df.loc[~is_home & (df["FTR"] == "A"), "points"] = 3
    df.loc[df["FTR"] == "D", "points"] = 1
    df = df.drop(columns="FTR")
    return df

def Convert_to_homeaway(df):
    #1 for home, 0 for away
    is_home = df["HomeTeam"] == "Real Madrid"
    df["is_home"] = 0
    df.loc[is_home, "is_home"] = 1
    df["opponent"] = df["AwayTeam"]
    df.loc[df["is_home"] == 0, "opponent"] = df["HomeTeam"]
    df["GF"] = df["FTAG"]
    df.loc[df["is_home"]==1,"GF"] = df["FTHG"]
    df["GA"] = df["FTAG"]
    df.loc[df["is_home"]==0,"GA"] = df["FTHG"]
    df["GD"] = df["GF"] - df["GA"]
    df["SF"] = df["AS"]
    df.loc[df["is_home"]==1,"SF"] = df["HS"]
    df["SA"] = df["AS"]
    df.loc[df["is_home"]==0,"SA"] = df["HS"]
    df["SD"] = df["SF"] - df["SA"]
    df["SoTF"] = df["AST"]
    df.loc[df["is_home"]==1,"SoTF"] = df["HST"]
    df["SoTA"] = df["AST"]
    df.loc[df["is_home"]==0,"SoTA"] = df["HST"]
    #df["SoT%"] = (df["SoTF"] / df["SF"]) * 100
    return df

def form_last5_games(df):
    #Total points last 5 games (10 is max, 0 is min)
    #Goal difference last 5 games
    #Shot difference last 5 games
    df["points_last_5_games"] = df["points"].shift(1).rolling(5,min_periods=5).sum()
    df["GD_last_5_games"] = df["GD"].shift(1).rolling(5,min_periods=5).sum()
    df["SD_last_5_games"] = df["SD"].shift(1).rolling(5,min_periods=5).sum()
    df["SoTF_last_5_games"] = df["SoTF"].shift(1).rolling(5,min_periods=5).mean()
    return df
    
def format_columns(df):
    df.style.format(
    {
        'points_last_5_games':'{:.0f}',
        'GD_last_5_games':'{:.0f}',
        'GD_last_5_games':'£{:.0f}',
        'SoT%':'{:.2%}'
    }
        )
    return df

"""df = madrid_filter(df)
df = clean_dataset(df)
df = Convert_to_homeaway(df)
df = convert_res_to_points(df)
df = form_last5_games(df)
df = drop_changed_columns(df)"""

def print_info(df):
    print(df.head(10))
    print(len(df))
    print(df["points_last_5_games"].mean())
    print(df.columns)

def load_raw_laliga():
    df_2020 = pd.read_csv(FILE_20_21, sep=",")
    df_2021 = pd.read_csv(FILE_21_22, sep=",")
    df_2022 = pd.read_csv(FILE_22_23, sep=",")
    df_2023 = pd.read_csv(FILE_23_24, sep=",")
    df_2024 = pd.read_csv(FILE_24_25, sep=",")
    return pd.concat([df_2020, df_2021, df_2022, df_2023, df_2024], ignore_index=True)

def build_madrid_df(df):
    df = madrid_filter(df)
    df = clean_dataset(df)
    df = Convert_to_homeaway(df)
    df = convert_res_to_points(df)
    df = form_last5_games(df)
    df = drop_changed_columns(df)
    return df

if __name__ == "__main__":
    df_raw = load_raw_laliga()
    df_madrid = build_madrid_df(df_raw)
    print_info(df)
    df_madrid.to_parquet("csv/processed/rm_matches.parquet", index=False)