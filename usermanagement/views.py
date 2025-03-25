from rest_framework_simplejwt.tokens import RefreshToken , AccessToken
from rest_framework.views import APIView
from . serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate



class RegisterUserView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data =data)
        if serializer.is_valid():
            data = serializer.validated_data
            username = data.get('mobile')

            password = data.get('password')
            user = authenticate(username=username, password=password)
            userserializer = UserSerializer(user)
            print(username , password)
            if user is None:
                print("error here")
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
            refresh  = RefreshToken.for_user(user)
            access = str(refresh.access_token)
            access_token = AccessToken(access)
            expiration_timestamp = access_token['exp']
            response = Response(userserializer.data , status=status.HTTP_200_OK)
            response.set_cookie('refresh_token', str(refresh) , httponly=True , samesite="None" , secure=True)
            response.set_cookie(key='access_token',  value = access, secure=True , httponly=True , samesite= "None")
            response.set_cookie(key='expiry', value=expiration_timestamp, secure=True, httponly=False, samesite="None")
            return response
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    






class RefreshTokenView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        token = request.COOKIES.get('refresh_token')
        old_access_token = request.COOKIES.get('access_token')

        if not token or not old_access_token:
            return Response({'error': 'Refresh token not provided'}, status=status.HTTP_403_FORBIDDEN)
        try:
            old_access_token = AccessToken(old_access_token)
            old_access_token.check_exp()
            return Response({'error': 'Access token is still valid'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass  

        try:
            refresh = RefreshToken(token)
            access = str(refresh.access_token)
            access_token = AccessToken(access)
            expiration_timestamp = access_token['exp']
            response = Response(status=status.HTTP_200_OK)
            response.set_cookie('refresh_token', str(refresh) , httponly=True , samesite="None" , secure=True)
            response.set_cookie(key='access_token',  value = access, secure=True , httponly=True , samesite= "None")
            response.set_cookie(key='expiry', value=expiration_timestamp, secure=True, httponly=False, samesite="None")
            return response

        except Exception as e: 
            response = Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            response.delete_cookie('refresh_token', domain=None)
            response.delete_cookie('access_token', domain=None)
            response.delete_cookie('expiry', domain=None)
            return response



class UserView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutView(APIView):
    def post(self, request):
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie('refresh_token', domain=None)
        response.delete_cookie('access_token', domain=None)
        response.delete_cookie('expiry', domain=None)
        return response