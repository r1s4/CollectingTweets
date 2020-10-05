import pandas as pd

df = pd.read_csv("./coronavirus.csv")
df = df[["user_id"]]
#df = df[1:]

df.to_csv('user_id.csv', index=False,header=False)
