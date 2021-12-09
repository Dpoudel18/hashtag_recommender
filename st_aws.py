import streamlit as st
from recommender import *



st.title('Twitter Hashtag Recommendation')
st.sidebar.header("Trending Twitter hashtags (US)")
trends_US = api.get_place_trends(23424977)
trends_world = api.get_place_trends(1)
topic_US = []
topic_World = []

for i in trends_US:
    for trend in i['trends']:
        topic_US.append(trend['name'])
for i in topic_US:
    if i.startswith('#'):
        st.sidebar.write(i)

st.sidebar.header("Trending Twitter hashtags (World)")
for i in trends_world:
    for trend in i['trends']:
        topic_World.append(trend['name'])
for i in topic_World:
    if i.startswith('#'):
        st.sidebar.write(i)

st.subheader('Write a tweet:')

tweet_input = st.text_input("")

appropriate_hashtag_list = hashtag_recommender(tweet_input)

if tweet_input != "":
    st.subheader('Recommended hashtag using Naive Bayes Model:')
    recommended_hashtags = " ".join(appropriate_hashtag_list)
    st.write(recommended_hashtags)