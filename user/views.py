from django.shortcuts import get_object_or_404
from .models import NewUser, Profile
from .serializers import UserSerializer, NewUserSerializer, LoginSerializer, UpdateSerializer
from .tasks import activate_email
from .decorators import error_catch
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.decorators import method_decorator

# Create your views here.
def security_set(request):
    return 'https' if request.is_secure() else 'http'
class UserRegister(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @method_decorator(error_catch)
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = NewUser.objects.get(email=email)
                user_data = NewUserSerializer(user)
                if not user.is_active:
                    activate_email.delay(security_set(request), get_current_site(request).domain, user_data.data, email)
                    return Response({"message":"please check your email for an activation link"}, status=status.HTTP_200_OK)
            except NewUser.DoesNotExist:
                pass
            else:
                return Response({"error":"This user already exists!"}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            email = serializer.validated_data["email"]
            user = get_object_or_404(NewUser, email=email)
            user_data = NewUserSerializer(user)
            activate_email.delay(security_set(request), get_current_site(request).domain, user_data.data, email)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            instance = NewUser.objects.get(id=pk)
        except NewUser.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
class UserLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data= request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            serializer = NewUserSerializer(user)
            token = RefreshToken.for_user(user)
            data = serializer.data
            data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLogout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST) 