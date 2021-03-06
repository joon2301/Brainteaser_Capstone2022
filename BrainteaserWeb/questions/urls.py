from django.urls import path 
from . import views 


appname='questions'

urlpatterns = [
    path('<str:t>/', views.list, name='list'),
    path('<str:t>/write', views.write, name='write'),
    path('<str:t>/write/test=<str:test>', views.titleTest, name='titleTest'),

    path('<str:t>/post=<int:p>', views.view, name='view'),
    path('<str:t>/post=<int:p>/parentAns', views.parentAns, name='parentAns'),
    path('<str:t>/post=<int:p>/childAns=<int:c>', views.childAns, name='childAns'),

    path('<str:t>/post=<int:p>/del', views.delete, name='delete'),
    path('<str:t>/post=<int:p>/comment=<int:c>/del', views.delComment, name='commentDel'),
    path('<str:t>/post=<int:p>/comment=<int:c>/edit', views.editComment, name='commentEdit'),
    path('<str:t>/post=<int:p>/comment=<int:c>/like', views.likeAnswer, name='commentLike'),
    path('<str:t>/post=<int:p>/comment=<int:c>/sim', views.simAnswer, name='commentLike'),
    path('<str:t>/post=<int:p>/edit/',views.edit, name='postEdit')


]

