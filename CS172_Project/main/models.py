from django.db import models
from .search import TweetIndex
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Tweets(models.Model):
    hash_tag = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    tweet_id = models.IntegerField()
    retweet_count = models.IntegerField()
    user_name = models.CharField(max_length=200)
    tweet_text = models.TextField()
    favorite_count = models.IntegerField()
    objects = models.Manager() # to get rid of warning
    # Add indexing method to Tweets
    # returns Tweets index and gets 
    # saved to ElasticSearch 
    def indexing(self):
        obj = TweetIndex(meta={'id': self.tweet_id},
                         hash_tag=self.hash_tag,
                         location=self.location,
                         tweet_id=self.tweet_id,
                         retweet_count=self.retweet_count,
                         user_name=self.user_name,
                         tweet_text=self.tweet_text,
                         favorite_count=self.favorite_count)
        obj.save()
        return obj.to_dict(include_meta=True)
# Create receiver
@receiver(post_save, sender=Tweets)
def index_tweet(sender, instance, **kwargs):
    instance.indexing()
