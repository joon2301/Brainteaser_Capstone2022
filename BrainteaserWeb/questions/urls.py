from django.urls import path 
from . import views 


appname='questions'

urlpatterns = [
    path('list/', views.list, name='list'),
    path('list/write', views.write, name='write'),
    path('list/post=<int:p>', views.view, name='view'),
    path('write/', views.write, name='write'),

            
            
]

