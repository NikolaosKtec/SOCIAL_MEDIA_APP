from django.contrib.auth.hashers import  make_password

from rest_framework import serializers

from django.contrib.auth import get_user_model
from .models import PostModel
from rest_framework.serializers import ValidationError

class PostModelSerializer(serializers.ModelSerializer):

   
    class Meta:
        model = PostModel
        fields = ['id','title','text','image','likes','was_created','user']
        
        extra_kwargs = {
        'id': {'required': False},
        
        'image': {'required': False},

        'was_created': {'required': False},
        
        'likes': {'required': False},
        
        
        }
        
    def validate_image_size(self):
        max_size_kb = 1 * 1024  # 1 KB
        if self.image.size > max_size_kb * 1024:
            raise ValidationError(f"O tamanho da imagem não pode exceder {max_size_kb} KB.")


class UserSerializer(serializers.ModelSerializer):

    posts = PostModelSerializer(read_only=True,many=True)

    class Meta:
        model = get_user_model()
        fields = ['id','username','email','password','followers','posts']
        
        extra_kwargs = {
        'password': {'write_only': True},
        
        'posts': {'required': False},
        'followers': {'required': False}
        }
    def validatePassword(self, raw_password):

        if len(raw_password) < 8:
            raise serializers.ValidationError("A senha deve ter pelo menos 8 caracteres.")
        
    def make_password(self):
        
        self.password = make_password( self._validated_data.get('password') )
           
    # def validate(self,*,title,text,user):
        
    #     # if title == "":
    #     #     raise serializers.ValidationError("Title não pode ser nulo!")
    #     if len(title) > 64:
    #         raise serializers.ValidationError("Title é muito longo!")
    #     if len(title) < 4:
    #         raise serializers.ValidationError("Title é muito curto!")
        
    #     if len(text) > 255:
    #         raise serializers.ValidationError("Text é muito longo!")
        
        
        # return True
class ObtainTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()