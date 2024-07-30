from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_spectacular.utils import extend_schema
from .serializers import RegisterSerializer

# Create your views here.


@extend_schema(
    tags=["Accounts"],
    description="회원가입 API",
    request=RegisterSerializer,
)
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=["Accounts"],
    description="로그인 API",
    request=TokenObtainPairSerializer,
)
class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = TokenObtainPairSerializer

    def post(self, request):
        User = get_user_model()
        username = request.data["username"]
        password = request.data["password"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"message": "존재하지 않는 아이디입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not check_password(password, user.password):
            return Response(
                {"message": "잘못된 비밀번호입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token = TokenObtainPairSerializer.get_token(user)
        access_token = str(token.access_token)

        return Response({"token": access_token}, status=status.HTTP_200_OK)
