# import packages

# packages lists
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
import tweepy
import pandas as pd
import numpy as np
import time
import pprint
import json
import matplotlib
import matplotlib.pyplot as plt
import seaborn
from config import (consumer_key, consumer_secret,
                    access_token, access_token_secret)

# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# Target User Account
target_users = [ "BBCNews",
"CBSNews",
"CNN",
"FoxNews",
"nytimes"]


# THIS CELL WILL GRAB THE "", "", AND "" VALUES AND PUT THEM INTO THE LISTS MADE IN THE PREVIOUS CELL 
#pretty print
pp = pprint.PrettyPrinter(indent=4)

#create the dictionary that we will put our columns (as lists) in
counter = 0

tweet_data = {"twt_source": [],
             "twt_text": [],
             "twt_date": [],
             "twt_vader": [],
             "twt_neg":  [],
             "twt_pos": [],
              "twt_neu": [],
            "twt_counter": []}

#second for loop, basically will loop through the different news sources
for users in target_users:

    # Loop through 5 pages of tweets (total 100 tweets per target user)
    for x in range(0, 5):
        public_tweets = api.user_timeline(users, page = x )

        #another for loop
        for tweet in public_tweets:
            tweet_data["twt_source"].append(tweet["user"]["name"])
            tweet_data["twt_text"].append(tweet["text"])
            tweet_data["twt_date"].append(tweet["created_at"])
            tweet_data["twt_counter"].append(counter)

            tweet_data["twt_vader"].append(analyzer.polarity_scores(tweet_data["twt_text"][counter])["compound"])
            tweet_data["twt_neg"].append(analyzer.polarity_scores(tweet_data["twt_text"][counter])["neg"])
            tweet_data["twt_pos"].append(analyzer.polarity_scores(tweet_data["twt_text"][counter])["pos"])
            tweet_data["twt_neu"].append(analyzer.polarity_scores(tweet_data["twt_text"][counter])["neu"])
            counter = counter + 1

            #pp.pprint(tweet)
            #print(tweet_data["twt_text"][0])
            # Run analysis
            # test = analyzer.polarity_scores(tweet_data["twt_text"][0])["neu"]
            # print(test)

            #pp.pprint(tweet_data["twt_text"])

# plot the first
# put the dictionary into a data frame
tweet_data_df = pd.DataFrame.from_dict(tweet_data)
tweet_data_df["twt_source"].unique()

tweet_data_df.head(5) # this will display the first 5 rows of the dataframe


#OK - now that I have the plot looking kind of like how I want it - I
# want to have the actual tweets ago column.  I'll make it from the twt_
# counter column
tweet_data_df['tweets_ago'] = abs(tweet_data_df['twt_counter'] - 100)
# tweet_data_df # commented this out - as it just puts the same dataframe as line 80

# plotting the scatter plot
# first I want to have the column header names (to identify x, y)
### list(tweet_data_df)
# now let's make new dataframes based upon the tweet source
bbc = tweet_data_df['twt_source'] == "BBC News (UK)"
cbs = tweet_data_df['twt_source'] == "CBS News"
cnn = tweet_data_df['twt_source'] == "CNN"
fox = tweet_data_df['twt_source'] == "Fox News"
nyt = tweet_data_df['twt_source'] == "The New York Times"
#tweet_data_df[nyt]

### Now I can try and define the one X and multiple Y axis
### based on the new dataframes

# x axes
x_bbc = tweet_data_df[bbc].twt_counter
x_cbs = tweet_data_df[cbs].twt_counter - 100
x_cnn = tweet_data_df[cnn].twt_counter - 200
x_fox = tweet_data_df[fox].twt_counter - 300
x_nyt = tweet_data_df[nyt].twt_counter - 400

# y axes
y_bbc = tweet_data_df[bbc].twt_vader
y_cbs = tweet_data_df[cbs].twt_vader
y_cnn = tweet_data_df[cnn].twt_vader
y_fox = tweet_data_df[fox].twt_vader
y_nyt = tweet_data_df[nyt].twt_vader

# now overwrite the default x-label
plt.scatter(x_bbc, y_bbc, label = "BBC")
plt.scatter(x_cbs, y_cbs, label = "CBS")
plt.scatter(x_cnn, y_cnn, label = "CNN")
plt.scatter(x_fox, y_fox, label = "Fox")
plt.scatter(x_nyt, y_nyt, label = "NY Times")
plt.legend(loc="upper left", bbox_to_anchor=(1,1))
plt.title(f"Sentiment Analysis of Media Tweets")
plt.xlim([x_bbc.max()+5, x_bbc.min()-5])
plt.ylabel("Tweet Polarity")
plt.xlabel("Tweets Ago")

plt.show()
