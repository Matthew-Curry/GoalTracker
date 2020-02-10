#############Serializers for Accounts App API#################################
#import serializers
from rest_framework import serializers
#the custom user model
from accounts.models import CustomUser
from rest_framework import serializers
#for overwriting the rest serializer
from rest_auth.serializers import LoginSerializer as RestAuthLoginSerializer
from rest_auth.registration.serializers import RegisterSerializer

#the Account Serializer
class UserSerializer(serializers.ModelSerializer):
    #the meta class
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

#The custom serializer for the login api, username set to none
class CustomLoginSerializer(RestAuthLoginSerializer):
    username = None
    email = serializers.EmailField(required = True, allow_blank = False)

#The custom serializer for the registration api, no username
class CustomRegisterSerializer(RegisterSerializer):
    username = None
    
    

