# this file was created by developer (not django generic)
from . import views
from django.urls import path


urlpatterns = [
    # empty string for default home page
    # .as_view() method must be add if using class based views
    path('', views.PostList.as_view(), name='home'),
]