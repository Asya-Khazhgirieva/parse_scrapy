#Подготовка файла, полученного после работы скрипта parse_scrapy.py, для импорта на сайт

import pandas as pd

path = "file.csv"
df = pd.read_csv(path, encoding="ANSI", sep=";")
for elem in df.ncTitle:
    if len(elem)+2 > 90:
        print(f"Слишком длинный заголовок {elem}")

df["Keyword"] = df["Keyword"].apply(str)

df["Keyword"] = df["Keyword"].str.replace("_", "-")
df["Keyword"] = df["Keyword"].str.replace(".", "-")
df["Keyword"] = df["Keyword"].str.replace(" ", "-")
df["Keyword"] = df["Keyword"].str.replace(",", "-")
df["Keyword"] = df["Keyword"].str.replace(";", "-")
df["Keyword"] = df["Keyword"].str.replace(":", "-")
df["Keyword"] = df["Keyword"].str.replace("(", "-")
df["Keyword"] = df["Keyword"].str.replace(")", "-")
df["Keyword"] = df["Keyword"].str.replace("=", "-")
df["Keyword"] = df["Keyword"].str.replace("/", "-")
df["Keyword"] = df["Keyword"].str.replace("--", "-")

df.loc[df.Description == df.Details, "Details"] = ""

df.to_csv(path, sep=";", index=False, encoding="ANSI")