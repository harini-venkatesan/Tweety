from elasticsearch_dsl.connections import connections 
from elasticsearch_dsl import Document, Text, Integer, Search
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models

# Create connection between Django app and ElasticSearch
connections.create_connection()

# Define what I want to index
class TweetIndex(Document):
    hash_tag = Text()
    location = Text()
    tweet_id = Integer()
    retweet_count = Integer()
    user_name = Text()
    tweet_text = Text()
    favorite_count = Integer()

    class Index:
        index = 'Tweet-index'
        name = 'tweet-index'
# Define function to do bulk indexing when
# something changes
def bulk_indexing():
    TweetIndex.init(index='Tweet-index') # Map model to ElasticSearch
    es = Elasticsearch() # Create connection to ElasticSearch
    # Iterate over all Tweet objects
    bulk(client=es, actions=(t.indexing() for t in models.Tweets.objects.all().iterator()))

def search(tweet_text):
    s = Search().filter('term', tweet_text=tweet_text)
    response = s.execute()
    return response