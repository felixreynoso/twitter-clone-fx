from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(TwitterUser)
admin.site.register(Tweet)
admin.site.register(Like)
# admin.site.register(RetweetTweet)
# admin.site.register(ReplyTweet)
# admin.site.register(QuoteTweet)
admin.site.register(Follow)
admin.site.register(Chat)
admin.site.register(Message)
