import pandas as pd
df = pd.read_parquet("csv/processed/rm_matches.parquet")


def make_target_3class(df):
    df = df.copy()
    # 2=win, 1=draw, 0=loss
    df["y"] = df["points"].map({3: 2, 1: 1, 0: 0}).astype("int8")
    return df

def remove_irrelevant_columns(df):
    columns_to_drop = [ 'GF', 'GA', 'GD', 'SF', 'SA',
       'SD', 'SoTF', 'SoTA', 'points']
    df = df.drop(columns=columns_to_drop)
    return df

def remove_missing_vals(df):
    df = df.dropna()
    return df

def concat_features(df):
    df2 = pd.concat([df["points_last_5_games"],df["GD_last_5_games"],df["SD_last_5_games"],df["SoTF_last_5_games"]],axis=1,join="outer")
    df2['Data'] = df[df2.columns].apply(
    lambda x: ','.join(x.dropna().astype(str)),
    axis=1
    )
    df3 = pd.concat([df2["Data"],df["y"]],axis=1)
    df3["Data"] = df3["Data"].apply(lambda s: [float(x) for x in s.split(',')])
    return df3

def engineer_features(df):
    df = pd.read_parquet("csv/processed/rm_matches.parquet")
    print(df.columns)
    df = make_target_3class(df)
    df = remove_irrelevant_columns(df)
    print(len(df))
    print(df.isnull().mean())
    df = remove_missing_vals(df)
    print(len(df))
    #df = concat_features(df)
    return df

if __name__ == "__main__":
    df = engineer_features(df)
    print(df.head(10))
    df.to_parquet("csv/processed/rm_features.parquet", index=False)