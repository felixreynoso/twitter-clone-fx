from django.urls import path
from . import views
from django.views.generic import RedirectView

app_name = 'feed'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('messages/', views.messages, name='messages'),
    path('tweet/', views.tweet, name='tweet'),
    path('like/<int:id>/', views.like, name='like'),
    path('follow/<int:id>/', views.follow, name='follow'),
    path('retweet/<int:id>/', views.retweet, name='retweet'),
    path('', RedirectView.as_view(url='home/')),
]
