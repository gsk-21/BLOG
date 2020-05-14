from django.urls import path
from . import views

urlpatterns = [
    path('',views.Home.as_view(),name='home'),

    path('about/', views.AboutUser.as_view(), name='about'),

    path('edit-user/', views.user_edit, name='edit-user'),

    path('register/',views.user_registration,name='register'),

    path('login/',views.user_login, name='login'),

    path('logout/',views.user_logout, name='logout'),

    path('post/',views.CreatePost.as_view(),name='create-post'),

    path('new-comments/', views.UnAppovedComments.as_view(), name='comments-to-approve'),

    path('drafts/',views.DraftList.as_view(),name='drafts'),

    path('all-posts/',views.ListPost.as_view(),name='list-posts'),

    path('<int:pk>/', views.PublicPostDetail.as_view(), name='public-post-detail'),

    path('all-posts/<int:pk>/',views.PostDetail.as_view(),name='post-detail'),

    path('all-posts/<int:pk>/update-post/',views.UpdatePost.as_view(),name='update-post'),

    path('all-posts/<int:pk>/delete-post/',views.DeletePost.as_view(),name='delete-post'),

    path('all-posts/<int:pk>/publish/', views.publish_post, name='publish-post'),

    path('<int:pk>/add-comment/', views.add_comment, name='add-comment'),

    path('all-posts/<int:pk>/comments/', views.comment_list, name='comment-list'),

    path('all-posts/<int:pk>/comments/approve-comment/', views.comment_approve, name='approve-comment'),

    path('all-posts/<int:pk>/comments/delete-comment/', views.comment_delete, name='delete-comment'),
]