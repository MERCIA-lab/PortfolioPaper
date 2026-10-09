from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserCreateSerializer, UserSerializer
from .services import user_create

class RegisterView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = user_create(**serializer.validated_data)
        
        return Response(
            UserSerializer(user).data, 
            status=status.HTTP_201_CREATED
        )


class UserView(APIView):   
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)