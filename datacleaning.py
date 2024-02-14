import pandas as pd 


d = pd.read_csv("top_50.csv", skiprows=1)
d["clean_title"] = d["Title"].apply(lambda x: x.split("  ")[0])
# print(d.head())

def pull_from_mal(n=50):
    tmp = pd.read_html("https://myanimelist.net/topanime.php")
    tmp[0].to_csv(f"top_{n}.csv")

def clean_data(f):
    df = pd.read_csv(f, skiprows=1)
    df["clean_title"] = df["Title"].apply(lambda x: x.split("  ")[0])
    return df