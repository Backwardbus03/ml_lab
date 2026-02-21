import pandas as pd

df = pd.read_csv("data\\athlete_events.csv")
regions = pd.read_csv("data\\noc_regions.csv")

def preprocess(df):
    df = df.merge(regions, how="left", left_on="NOC", right_on="NOC")
    df = df[df["Season"] == "Summer"]
    df.drop_duplicates(inplace=True)
    df = pd.concat([df, pd.get_dummies(df["Medal"])], axis=1)
    return df