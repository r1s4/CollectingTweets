import pandas as pd

df_tweet = pd.read_csv('./coronavirus.csv')
df_tweet = df_tweet.set_index('user_id')

def main():
    df_RT=df_tweet[df_tweet['RT']>00]
    
    df_RT.to_csv("RT_over100.csv")

if __name__ == "__main__":
	main()