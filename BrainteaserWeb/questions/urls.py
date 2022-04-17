from django.urls import path 
from . import views 


appname='questions'

urlpatterns = [
    path('list/', views.list, name='list'),
    path('list/write', views.write, name='write'),

    path('list/post=<int:p>', views.view, name='view'),
    path('list/post=<int:p>/comment=<int:c>/del', views.delComment, name='commentDel'),
    path('list/post=<int:p>/comment=<int:c>/edit', views.editComment, name='commentDel'),

    path('list/post=<int:p>/edit/',views.edit, name='postEdit')


]

