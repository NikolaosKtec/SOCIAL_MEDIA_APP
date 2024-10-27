from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from rest_framework.serializers import ValidationError





class UserModel(AbstractUser):
    # class Meta:
    #         verbose_name = 'UserModel'
    #         verbose_name_plural = 'UsersModel'
    
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=256)
    wasCreated = models.DateTimeField(auto_now_add=True)
    #NOTE para fins de desenvolvimento, n° seguidores foi limitado
    #  followers list -> id_user
    followers = models.TextField(max_length=1024, blank=True)
    

    def __str__(self):
        return self.username
    
    def isDuplicatedFollowers(self,new):

        list = self.getFollowersList() #cast to list
        if list.count(str(new)) > 0:
            return True
        else:
            return False

    def addFollowers(self, new):
        
        if self.isDuplicatedFollowers(new):
            raise ValidationError("This follower already exists on your list!")
        self.followers +=str(new)+','

    def removeFollowers(self, new):
        index = self.followers.find(str(new))
        if index == -1:
            raise ValidationError("There is no such follower on your list!")
        elif( (index+1) == len(self.followers)): #last occours
            index -= 1
            self.followers = self.followers[0:index]
        else:
            # Remove o 3 seguido de vírgula
            self.followers = self.followers.replace(str(new) + ',', '')  

    def getFollowersList(self):
        
        if not self.followers == "":
            return self.followers.split(',')
        return []

class PostModel(models.Model):
        
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE, related_name='posts')
    was_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=64)
    text= models.CharField(max_length=512,blank=True)
    image = models.ImageField(blank=True,storage='/content/images')
    likes = models.IntegerField(blank=True,default=0)

    # class Meta:
    #     # unique_together = ['user','title']
    #     ordering = ['was_created']
            
    def __str__(self):
        return self.title
    def addLike(self):
        self.likes += 1

    
        