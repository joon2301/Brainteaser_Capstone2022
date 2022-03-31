from django.urls import include, path 
from . import views 


from django.urls import path
from .views import * # user>views에서 모든 함수를 가져온다.
from django.contrib.auth import views as auth_views

app_name = "users"
urlpatterns = [
    path("", views.main, name='main'),
]