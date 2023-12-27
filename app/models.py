from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from rest_framework.validators import ValidationError
from django.contrib.auth import get_user_model
from project import settings

# User = get_user_model()
    

class CustomUserManager(BaseUserManager):

    def create_user(self,email,password,**extra_fields):
        email = self.normalize_email(email=email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)

        if extra_fields.get('is_superuser') is not True:
            raise ValidationError('super user must have is_superuser to be True')
        return self.create(email=email,password=password,**extra_fields)
    

class User(AbstractUser):
    email = models.EmailField()
    username = models.CharField(max_length=10,unique=True)
    date_of_birth = models.DateField(null=True)
    followers = models.ManyToManyField('self',symmetrical=False,blank=True, related_name='following')
    
    @property
    def following_count(self):
        return self.following.count()
    
    @property
    def followers_count(self):
        return self.followers.count()


    objects = CustomUserManager()

    REQUIRED_FIELDS =['email']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content