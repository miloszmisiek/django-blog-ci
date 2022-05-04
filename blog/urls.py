# this file was created by developer (not django generic)
from . import views
from django.urls import path


urlpatterns = [
    # empty string for default home page
    # .as_view() method must be add if using class based views
    path('', views.PostList.as_view(), name='home'),
    # first slug is path converter, second is keyword name from views.py
    # pathconverter converts keyword into the slug field
    # it's built-in django feature, it tells django to match any slug string, which consists of ASCII characters...
    # ... numbers plus hyphen and underscore characters
    path('<slug:slug>', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
]