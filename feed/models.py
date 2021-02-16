from django.db import models
from datetime import datetime

from django.contrib.auth.models import User


# Create your models here.
class Tweet(models.Model):
    post_date = models.DateTimeField("Posted On",auto_now_add=True)
    author = models.ForeignKey('TwitterUser', on_delete=models.CASCADE)
    text = models.TextField(max_length=351, blank=True)
    replies_to = models.ForeignKey('Tweet', blank=True, on_delete=models.CASCADE,related_name='replies', null=True, default=None)
    quotes = models.ForeignKey('Tweet', blank=True, on_delete=models.CASCADE, related_name='quotes_set', null=True, default=None)
    retweets_to = models.ForeignKey('Tweet', blank=True, on_delete=models.CASCADE, related_name='retweets_to_set', null=True, default=None)

    def __str__(self):
        return f"{self.text[:15]}... by: {self.author}"

    class meta():
        ordering = ['-post_date']

    @property
    def likes_count(self):
        return len(self.like_set.all())

    @property
    def retweets_count(self):
        return len(self.retweets_to_set.all())

    @property
    def replies_count(self):
        return len(self.replies.all())



class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author} likes "{self.tweet}" by: {self.tweet.author}'


class TwitterUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, null=True)
    followers_count = models.IntegerField(default=0)
    follows = models.ManyToManyField('Follow', blank=True, default=None)

    def __str__(self):
        return self.user.username

    class meta():
        ordering = ['user']

    @property
    def tweets(self):
        #saves all the tweets by author in result
        result = Tweet.objects.filter(author=self.user.twitteruser)
        # concatenates result with all the tweets twitterusers this user follows

        friends_tweets = []
        for friend in self.follows.all():
            friends_tweets.append(friend.target.tweet_set.all())

        result = result.union(*friends_tweets)
        #returns all the tweets relevant to this user ordered from new to old
        return (result.order_by('-post_date'))

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Follow(models.Model):
    target = models.ForeignKey(TwitterUser, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return "Target: " + self.target.user.username


class Chat(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    messages = models.ManyToManyField('Message', default=None, blank=True)
    members = models.ManyToManyField(TwitterUser)

    class meta():
        ordering = ('-created_at')
        # ordering = ('-messages')

    def __str__(self):
        members =  [member.user.username for member in self.members.all()]
        return f"Chat between {' and '.join(members)}"


class Message(models.Model):
    sent_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(TwitterUser, on_delete=models.CASCADE, null=False)
    message = models.TextField(max_length=5000)

    class meta():
        ordering = ('-sent_at')

    def __str__(self):
        return self.message[:20]+'...' + ' by ' + self.author.user.username
        # return self.message[:20]+'...' + ' by ' + self.author.user.username + ' - ' + str(self.chat_set.all()[0])
#
# class Notification(models.Model):
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     owner = models.ForeignKey(TwitterUser, on_delete=models.CASCADE, null=False)
#     actuator = models.ForeignKey(TwitterUser, on_delete=models.CASCADE, null=False, related_name='actuator')
#     actioned_obj_ref = models.TextField(max_length=500)
#     action_type =  models.TextField(max_length=50)



"""



from feed.models import *
fx = TwitterUser.objects.get(user=1)
fx.tweets













"""
