'''The Views for the User API'''
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.api.serializers import UserSerializer

#View that uses the serializer to take in the response input
class CurrentUserAPIView(APIView):
    def get(self, request):
        #the serializer
        serializer = UserSerializer(request.user)
        #return the data
        return Response(serializer.data)
