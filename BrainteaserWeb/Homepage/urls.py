from django.urls import path 
import Homepage.views 


appname='Homepage' 

urlpatterns = [ path('', Homepage.views.index, name='Home'), ]

