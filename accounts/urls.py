from django.conf.urls import include, url
from django.urls import path

from . import views
from .views import UserList, GoogleLogin, current_user

app_name = 'accounts'

urlpatterns = [
    path('rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('', UserList.as_view()),
    path('current', current_user),

    url(r'^search/$', views.Search.as_view(), name='search'),
    url(r'^explore/$', views.ExploreUsers.as_view(), name='explore_user'),
    url(r'^(?P<user_id>\d+)/follow/$', views.FollowUser.as_view(), name='follow_user'),
    url(r'^(?P<user_id>\d+)/unfollow/$', views.UnFollowUser.as_view(), name='unfollow_user'),
    url(r'^(?P<username>\w+)/followers/$', views.UserFollowers.as_view(), name='user_followers'),
    url(r'^(?P<username>\w+)/following/$', views.UserFollowing.as_view(), name='user_following'),
]
