"""
URL configuration for social_media_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.contrib import admin
from django.urls import path

from social_network.views import UserView,PostView,LoginView

# from rest_framework import routers
# route = routers.DefaultRouter()
# route.register('name',<*viewset>, basename=arg)



urlpatterns = [
    
    path('admin/', admin.site.urls),
    #  create and list users.
    path('users/',UserView.UserView.as_view()),
    # create and list posts.
    path('posts/',PostView.PostView.as_view()),
    # like a post, *id is the mandatory, target argument.
    path('posts/like/<int:id>/',PostView.LikePost.as_view()), 
    
    # authenticates users to use the API.
    path('login/',LoginView.LoginView.as_view() ),
    # follow a user, *id is the mandatory, target argument.
    path('users/follow/<int:id>/',UserView.FollowView.as_view() ),
    # unollow a user, *id is the mandatory, target argument.
    path('users/unfollow/<int:id>/',UserView.UnfollowView.as_view() ),
    # post feed.
    path('feed/',PostView.FeedView.as_view() )
]
