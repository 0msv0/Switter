from django.urls import path
from . import views

app_name = "userProfile"

urlpatterns = [
    path('homePage/', views.homepage, name='homePage'),
    path('myProfile/', views.myProfile, name='profile'),
    path('profile/<int:profileId>/', views.userProfile, name='user profile'),
    path('pdf/', views.GeneratePDF.as_view()),

    path('friend_request/', views.friend_request_page, name='friend request'),
    path('requestPage/', views.requestPage, name='request page'),

    path('send_friend_request/<int:userId>/', views.send_friend_request, name='send friend request'),
    path('accept_friend_request/<int:requestId>/', views.accept_friend_request, name='accept friend request'),
    path('reject_friend_request/<int:requestId>/', views.reject_friend_request, name='reject friend request'),
    path('delete_friend/<int:userId>/', views.delete_friend_request, name='delete friend'),

    path('friendlist/', views.friendList, name='friend list'),
    path('friendlist/<int:userId>/', views.userFriendList, name='user friend list'),

    path('post/new/', views.create_post, name='post-create'),
    path('myPosts/', views.postsView, name='posts view'),
    path('deletePost/<int:pk>/', views.post_delete, name='delete post'),
    path('posts/<int:userId>/', views.userPostView, name='user post view'),
    path('myPost/<int:pk>/', views.postDetail, name='post detail'),
    path('post/<int:userId>/<int:postId>/', views.userPostDetail, name='user post detail'),

    path('comment/new/<int:postId>/', views.createComment, name='new comment'),
    path('comment/new/<int:postId>/<int:commentId>/', views.createReplies, name='new reply'),
    path('replies/<int:commentId>/', views.showReplies, name='show replies'),

    path('addLike/<int:postId>/', views.addLike, name='add like'),
    path('addDislike/<int:postId>/', views.addDislike, name='add dislike'),

    # path('posts/', views.postViewSet, name='post list'),
    # path('post/<int:pk>/', views.postDetail, name='post detail'),
    # path('createPost/', views.postCreate, name='create post'),
    # path('deletePost/<int:pk>/', views.postDelete, name='delete post')

]
