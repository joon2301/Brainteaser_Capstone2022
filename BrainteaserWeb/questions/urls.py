from django.urls import path 
from . import views 


appname='questions'

urlpatterns = [
    path('<str:t>/', views.list, name='list'),
    path('<str:t>/write', views.write, name='write'),

    path('<str:t>/post=<int:p>', views.view, name='view'),
    path('<str:t>/post=<int:p>/comment=<int:c>/del', views.delComment, name='commentDel'),
    path('<str:t>/post=<int:p>/comment=<int:c>/edit', views.editComment, name='commentDel'),

    path('<str:t>/post=<int:p>/edit/',views.edit, name='postEdit')


]

