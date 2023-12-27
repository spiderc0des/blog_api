from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.authtoken.views import ObtainAuthToken

post_router = DefaultRouter()
my_post_router = DefaultRouter()

post_router.register('', views.PostViewSet, basename='post_view')
my_post_router.register('', views.MyPostView, basename='my_post')

urlpatterns = [
    path('post/', include(post_router.urls)),
    path('mypost/', include(my_post_router.urls)),
    path('signup/', views.SignUpView.as_view()),
    path('login/', ObtainAuthToken.as_view()),
    path('profile/', views.ProfileView.as_view()),
    path('follow/<str:username>/', views.follow),
    path('unfollow/<str:username>/', views.unfollow),
    path('users/', views.get_users),
    path('<int:post_id>/comment/', views.CommentView.as_view())

]