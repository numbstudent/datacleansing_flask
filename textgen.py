import pandas as pd
from random import randrange

df = pd.read_csv("archive/data.csv",encoding='latin-1')
def generate_text(counter, specialword):
    df_tweet = df.Tweet
    if counter.isdigit():
        if specialword:
            df_tweet = df_tweet.loc[df_tweet.str.contains(specialword)]
        df_tweet = df_tweet.reset_index(drop=True)
        df_final = pd.DataFrame()
        final_arr = []
        counter = int(counter)
        for x in range(0,counter):
            index = randrange(0,df_tweet.size)
            print(index)
            final_arr.append(df_tweet[index])
        df_final['Tweet'] = final_arr
        df_final = df_final.drop_duplicates()
        df_final.to_csv("archive/test_data.csv", index=False, header=False)
        return ("Random text generation completed. "+str(df_final.size)+" unique rows are generated.")
    else:
        return ("Please input integer!")