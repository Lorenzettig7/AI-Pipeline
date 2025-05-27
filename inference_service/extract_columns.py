import pandas as pd

df = pd.read_csv("cleaned_ddos.csv")
print("Columns:", df.columns.tolist())
print("Total:", len(df.columns))

