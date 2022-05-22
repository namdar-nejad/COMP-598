# Setup step
import pandas as pd

# read in the input datasset from the file
df = pd.read_csv('../data/inputdata.csv')

# read in the iput dataset from the url (this was taking way too long for me)
# df = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/russian-troll-tweets/master/IRAhandle_tweets_1.csv')

# droping the extra columns to have a cleaner dataframe
df = df.drop(['external_author_id', 'author', 'region', 'harvested_date',
              'following', 'followers', 'updates', 'post_type', 'account_type',
              'retweet', 'account_category', 'new_june_2018', 'alt_external_id', 
              'article_url', 'tco1_step1', 'tco2_step1', 'tco3_step1'], axis=1)

# function for truncation
import math
def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

# Q1

# top 10000
df_head = df.head(10000)

# english
df_en = df_head.loc[df_head['language'] == 'English']

# not Qs
df_q = df_en.loc[~df_en['content'].str.contains(pat = '\?', regex = True)]

# drop the language column since we are donw with it
df_final = df_q.drop(['language'], axis=1)

# fix column order
cols = df_final.columns.tolist()
df_final = df_final[['tweet_id', 'publish_date', 'content']]

# Save as tsv
with open('./data1.tsv','w') as write_tsv: write_tsv.write(df_final.to_csv(sep='\t', index=False))

# Q2

# use regex to find the tweets that mention Trump
df_trump = df_final['content'].str.contains(pat =
                                            '[^a-zA-Z]Trump[^a-zA-Z]|[^a-zA-Z]Trump$|^Trump[^a-zA-Z]|^Trump$', case=True, regex=True)

# add an extra column
df_final['trump_mention'] = df_trump

# write file
with open('../dataset.tsv','w') as write_tsv: write_tsv.write(df_final.to_csv(sep='\t', index=False))

# Q3

# calculate the fraction 
frac = (df_final.trump_mention.sum())/(df_final.shape[0])
frac = truncate(frac, 3)

# write to file
data = [['frac-trump-mentions', frac]]
res_df = pd.DataFrame(data, columns = ['result', 'value'])
with open('../results.tsv','w') as write_tsv: write_tsv.write(res_df.to_csv(sep='\t', index=False))
