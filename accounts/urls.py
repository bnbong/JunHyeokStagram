from django.conf.urls import include, url
from django.urls import path

from . import views


app_name = 'accounts'

urlpatterns = [
    path('rest-auth/google/', views.GoogleLogin.as_view(), name='google_login'),
    # path('', views.UserList.as_view()),
    # path('current', current_user),

    url(r'^search/$', views.Search.as_view(), name='search'),
    url(r'^explore/$', views.ExploreUsers.as_view(), name='explore_user'),
    url(r'^(?P<username>\w+)/$', views.UserProfile.as_view(), name='user_profile'),
    url(r'^(?P<user_id>\d+)/follow/$', views.FollowUser.as_view(), name='follow_user'),
    url(r'^(?P<user_id>\d+)/unfollow/$', views.UnFollowUser.as_view(), name='unfollow_user'),
    url(r'^(?P<username>\w+)/followers/$', views.UserFollowers.as_view(), name='user_followers'),
    url(r'^(?P<username>\w+)/following/$', views.UserFollowing.as_view(), name='user_following'),
    url(r'^(?P<user_id>\d+)/makefriend/$', views.MakeFriend.as_view(), name='friend_user'),
    url(r'^(?P<user_id>\d+)/deletefriend/$', views.DeleteFriend.as_view(), name='unfriend_user'),
    url(r'^(?P<username>\w+)/friends/$', views.UserFriends.as_view(), name='user_friends'),
]
