from django.urls import path 
from . import views 


appname='theme' 

urlpatterns = [
    path('index', views.index, name='index'),
    path('list/', views.list2, name='list'),
    path('next/', views.next, name='next'),

    path('list/write', views.write, name='write'),
    path('list/view', views.view, name='view'),
    path('write/', views.write, name='write'),
    path('logout/', views.logout, name='logout')

            
            
            
            
            
            
]

