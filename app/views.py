from rest_framework import viewsets
from .models import Post,User
from .serializers import PostSerializer,UserSerializer,CommentSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,AllowAny
from rest_framework.authentication import TokenAuthentication,BasicAuthentication
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action


class MyPostView(viewsets.ModelViewSet):
    authentication_classes=[TokenAuthentication,BasicAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user) 
    



# 
class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # @swagger_auto_schema(operation_summary="Get a list of all posts")
    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

    # @swagger_auto_schema(operation_summary="Create a new post")
    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)

    # @swagger_auto_schema(operation_summary="Retrieve a specific post")
    # def retrieve(self, request, *args, **kwargs):
    #     return super().retrieve(request, *args, **kwargs)

    # @swagger_auto_schema(operation_summary="Update a post")
    # def update(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)

    # @swagger_auto_schema(operation_summary="Partially update a post")
    # def partial_update(self, request, *args, **kwargs):
    #     return super().partial_update(request, *args, **kwargs)

    # @swagger_auto_schema(operation_summary="Delete a post")
    # def destroy(self, request, *args, **kwargs):
    #     return super().destroy(request, *args, **kwargs)

class SignUpView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def post(self,request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user

        response = {
            'username': user.username,
            'email': user.email,
            'date_of_birth': user.date_of_birth,
            'followers': user.followers_count,
            'following': user.following_count
        }
        return Response(response)
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def follow(request, username):
    user_to_follow = get_object_or_404(User,username=username)
    if user_to_follow != request.user:
        request.user.following.add(user_to_follow)
        return Response(data={'status':'following'}, status=status.HTTP_200_OK)
    else:
        return Response(data='can\'t follow self', status=status.HTTP_400_BAD_REQUEST)
    
@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def unfollow(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    if user_to_unfollow != request.user:
        request.user.following.remove(user_to_unfollow)
        return Response(f'unfollowed {user_to_unfollow}')
    else:
        return Response(data='can\'t unfollow self', status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication,BasicAuthentication])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(instance=users, many=True)
    return Response(serializer.data)


class CommentView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]
    serializer_class = CommentSerializer

    def post(self, request, post_id:int):
        content = request.data
        post = get_object_or_404(Post, pk=post_id)
        serializer = CommentSerializer(data=content)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)