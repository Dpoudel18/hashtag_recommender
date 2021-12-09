import tweepy
from rake_nltk import Rake
import tweepy
from collections import Counter
import re
from config import *

client = tweepy.Client(bearer_token)

def get_api():
    auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

api = get_api()


def extract_hashtags(text):
    hashtag_list = []
    for word in text.split():
        if word[0] == '#':
            hashtag_list.append(f'#{word[1:].lower()}')
    return hashtag_list

def extract_keywords(tweet):

    rake_nltk_var = Rake()
    rake_nltk_var.extract_keywords_from_text(tweet)
    keyword_extracted = rake_nltk_var.get_ranked_phrases()
    return keyword_extracted


def query_string(input_tweet):
    query_string = ""
    word_groupings = extract_keywords(input_tweet)
    for i in word_groupings:
        query_string += '('+i+')' + ' OR '
    query_string = query_string[:-4]
    return query_string

def hashtag_recommender(input_tweet):
    query = query_string(input_tweet)
    print(query)
    searched_tweets = []
    final_hashtag_list = []


    try:
        for tweet in tweepy.Paginator(client.search_recent_tweets,query, max_results=100).flatten(limit=1000):
            searched_tweets.append(tweet.text)
    except:
      pass

    searched_tweets_string = "".join(searched_tweets)

    hashtag_list = re.findall(r"#(\w+)", searched_tweets_string)

    for i in hashtag_list:

        final_hashtag_list.append(i[0].upper() + i[1:])

    word_count = Counter(final_hashtag_list)
    word_frequency_count = [key for key, _ in word_count.most_common(10)]

    hashtag_count = []
    for i in word_frequency_count:
        hashtag_count.append('#'+i)

    return hashtag_count