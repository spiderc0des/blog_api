from rest_framework import serializers
from .models import Post,User,Comment
from rest_framework.validators import ValidationError



class CommentSerializer(serializers.ModelSerializer):
    # post = serializers.ReadOnlyField(source='post.id')
    author = serializers.CharField(read_only=True)
    class Meta:
        model = Comment
        fields = ['content','created_on', 'author']


class PostSerializer(serializers.ModelSerializer):
    
    title = serializers.CharField(max_length=20)
    content = serializers.CharField()
    author = serializers.ReadOnlyField(source='author.username')

    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ['title','content','created_on','author','comments']
        

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(min_length=8,write_only=True)
    date_of_birth = serializers.DateField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()


    class Meta:
    
        model = User
        fields = ['email','username','password','date_of_birth','followers_count','following_count']


    def validate(self,attrs):
        email_exist = User.objects.filter(email=attrs['email']).exists()
        if email_exist:
            raise ValidationError('email already exist')
        
        username_exist = User.objects.filter(username=attrs['username']).exists()
        if username_exist:
            raise ValidationError('username already exist')
        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
    
# class UserDetailSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     username = serializers.CharField()
#     date_of_birth = serializers.DateField()
#     followers = UserSerializer(many=True)
#     following = UserSerializer(many=True)