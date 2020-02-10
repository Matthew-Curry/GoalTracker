from rest_auth.serializers import LoginSerializer as RestAuthLoginSerializer

#The custom serializer for the login api, username set to none
class LoginSerializer(RestAuthLoginSerializer):
    username = None