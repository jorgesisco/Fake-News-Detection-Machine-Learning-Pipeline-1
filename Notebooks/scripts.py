import pandas as pd
import re
import string
import tweepy
from dotenv import load_dotenv
import os


tweets = []
userID = []
tweetID = []
tweet_url = []
username = []
next_page_token = []


# Creating a function that will take the text from the dataset and remove special characters
def word_drop(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('\\W', " ", text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('https   t co ', '', text)
    text = re.sub('  ', ' ', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text



# Functions to Collect Data from Twitter

def getClient():
    
    client = tweepy.Client(bearer_token= os.getenv("BEARER_TOKEN"),
                           consumer_key=os.getenv("API_KEY"), 
                           consumer_secret=os.getenv("API_KEY_SECRET"), 
                           access_token=os.getenv("ACCESS_TOKEN"),
                           access_token_secret=os.getenv("ACCESS_TOKEN_SECRET"))

    return client


def searchTweets(query, qty):
    
    client = getClient() # First Function is called right here.
    client_call = client.search_all_tweets(query=query, max_results=qty, expansions='author_id') # API call to get the Data
    
    if not client_call.data is None and len(client_call.data) > 0: #Checking if there are results or not before looping...
        for tweet in client_call.data:
            tweets.append(tweet.text)        #Adding Tweets to the List created before           
            tweetID.append(tweet.id)         #Adding Tweets IDs to the List created before
            userID.append(tweet.author_id)   #Adding Users IDs to the List created before
            tweet_url.append('https://twitter.com/{}/status/{}'.format(tweet.author_id, tweet.id))
                          # ↑Adding Tweet URL to the List created before ↑
    else:
        return ['NO DATA WAS FOUND']
    
    # Using try and except to avoid getting erros in the script during the data collection
    try:
        next_page = client_call.meta['next_token']
        next_page_token.append(next_page)
    except KeyError:
        print("NO NEXT TOKEN AVAILABLE, THIS MEANS YOU GOT ONLY ONE PAGE.... :( ")

    df = pd.DataFrame({'Tweets': tweets, "Tweet URL": tweet_url, 'Tweet ID': tweetID, "User ID": userID})
           
    return df 


def search_tweets_next(query, qty, next_page_token, pagination):
    
    client = getClient() # First Function is called right here.

     # ↓ API call to get the Data ↓
    client_call_ = client.search_all_tweets(query=query, max_results=qty, expansions='author_id', next_token=next_page_token[pagination])
   
    if not client_call_.data is None and len(client_call_.data) > 0: #Checking if there are results or not before looping...
        for tweet in client_call_.data:
            tweets.append(tweet.text)        #Adding Tweets to the List created before
            tweetID.append(tweet.id)         #Adding Tweets IDs to the List created before
            userID.append(tweet.author_id)   #Adding Users IDs to the List created before
            tweet_url.append('https://twitter.com/{}/status/{}'.format(tweet.author_id, tweet.id))
                          # ↑Adding Tweet URL to the List created before ↑
    else:
        return ['NO DATA']
    # Using try and except to avoid getting erros in the script during the data collection
    try:
        next_page = client_call_.meta['next_token']
        next_page_token.append(next_page)
    except KeyError:
        print("NO NEXT TOKEN AVAILABLE, THIS MEANS YOU GOT UNTIL THIS PAGE:( .... :( ")
    
    df = pd.DataFrame({'Tweets': tweets, "Tweet URL": tweet_url, 'Tweet ID': tweetID, "User ID": userID})
        
    return df


def get_user_by_id(userID):
    
    client = getClient()
    client_call = client.get_user(id=userID)
    user_id = client_call.data.username
    
    return user_id
    

