from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import RegisterSerializer

# Create your views here.


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]


    def post(self, request):
        User = get_user_model()
        username = request.data["username"]
        password = request.data["password"]
        
        user = User.objects.get(username=username)
        if user is None:
            return Response({'message':'존재하지 않는 아이디입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not check_password(password, user.password):
            return Response({'message':'잘못된 비밀번호입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        token=TokenObtainPairSerializer.get_token(user)
        access_token=str(token.access_token)
        
        return Response({'token':access_token}, status=status.HTTP_200_OK)
        