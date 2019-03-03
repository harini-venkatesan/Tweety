from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json 
import sys
import collections
import re

reload(sys)
sys.setdefaultencoding('utf-8')


API_KEY = ''# add api_key from twitter account
SECRET_KEY = ''# add secret_key from twitter account

ACCESS_TOKEN = ''# add access token
ACCESS_TOKEN_SECRET = ''
fw = open('CS_data.json', 'a')

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_status(self, status):

    
        
        if(status.entities.get('hashtags')) == []:
            return

    
        else:
            if(not status.retweeted) and ('RT @' not in status.text):
                parsed_tweet = {'user_name': status.user.screen_name}
                parsed_tweet.update({'tweet_text': status.text})

                entities = status.entities
                hash_tags = []
                for item in entities.get('hashtags'):
                    hash_tags.append(item.get('text'))
                parsed_tweet.update({'hash_tags': hash_tags})

                parsed_tweet.update({'tweet_id': status.id})  
                parsed_tweet.update({'retweet_count': status.retweet_count})
                parsed_tweet.update({'favorite_count': status.favorite_count})                   
                parsed_tweet.update({'Location': status.user.location})
                print(parsed_tweet)
                fw.write(json.dumps(parsed_tweet))
                fw.write("\n")

        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

          
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(API_KEY, SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = Stream(auth, l, tweet_mode = 'extended')
    
    stream.filter(languages=["en"], track=['the','a','an'])


