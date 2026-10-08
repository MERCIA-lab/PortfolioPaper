from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserCreateSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class UserView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserCreateSerializer(user)
        return Response(serializer.data)