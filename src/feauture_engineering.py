import pandas as pd
df = pd.read_parquet("csv/processed/rm_matches.parquet")

print(df.head(10))
print(df["Date"])