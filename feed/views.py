from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.urls import reverse

# Create your views here.

def home(request):
    feed = list(Tweet.objects.order_by('-post_date'))
    return render(request, 'feed/home.html', {'feed': feed})

def tweet(request):
    tweet = request.POST['tweet']
    if tweet:
        request.user.twitteruser.tweet_set.create(text=tweet)

    return HttpResponseRedirect(reverse('feed:home'))

def retweet(request,id):
    rt = Tweet.objects.get(pk=id)
    Tweet.objects.create(author=request.user.twitteruser,retweets_to=rt)
    return HttpResponseRedirect(reverse('feed:home'))


def like(request, id):
    user = request.user
    tweet = Tweet.objects.get(pk=id)
    Like.objects.create(author=user, tweet=tweet)

    return HttpResponseRedirect(reverse('feed:home'))

def follow(request, id):
    followee = TwitterUser.objects.get(pk=id)
    follow = Follow.objects.create(target=followee)

    request.user.twitteruser.follows.add(follow)

    return HttpResponseRedirect(reverse('feed:home'))

def profile(request):
    user = request.user
    feed = user.twitteruser.tweets
    following_count = len(user.twitteruser.follows.all())
    return render(request, 'feed/profile.html',
                {'feed': feed,
                'following_count':following_count})


def messages(request):
    user = request.user
    chats = user.twitteruser.chat_set.all().order_by('-created_at')
    return render(request, 'feed/messages.html', {'chats':chats})
