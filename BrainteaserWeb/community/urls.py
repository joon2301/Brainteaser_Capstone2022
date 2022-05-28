from django.urls import path 
from . import views 


appname='community'

urlpatterns = [
    path('<str:t>/', views.list, name='list2'),
    path('<str:t>/write', views.write, name='write2'),
    path('<str:t>/write/test=<str:test>', views.titleTest, name='titleTest2'),

    path('<str:t>/post=<int:p>', views.view, name='view2'),
    path('<str:t>/post=<int:p>/parentAns', views.parentAns, name='parentAns2'),
    path('<str:t>/post=<int:p>/childAns=<int:c>', views.childAns, name='childAns2'),

    path('<str:t>/post=<int:p>/del', views.delete, name='delete2'),
    path('<str:t>/post=<int:p>/comment=<int:c>/del', views.delComment, name='commentDel2'),
    path('<str:t>/post=<int:p>/comment=<int:c>/edit', views.editComment, name='commentEdit2'),
    path('<str:t>/post=<int:p>/comment=<int:c>/like', views.likeComment, name='commentLike2'),
    path('<str:t>/post=<int:p>/comment=<int:c>/sim', views.simAnswer, name='commentLike2'),
    path('<str:t>/post=<int:p>/edit/',views.edit, name='postEdit2'),

]

