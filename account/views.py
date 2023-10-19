from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from account.forms import UserRegistrationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from account.models import UserProfile
from account.serializers import UserSerializer, RegisterSerializer
from rest_framework import viewsets, status
from django.contrib.auth import authenticate, login
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')


def referral_links(request):
    referrals = UserProfile.objects.filter(referral_email=request.user.email)
    return render(request, 'referral_links.html', {'referrals': referrals})


# --------------- api ---------------
class UserProfileApi(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get']


class RegisterApiView(APIView):
    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={status.HTTP_201_CREATED: 'Created', status.HTTP_400_BAD_REQUEST: 'Bad Request'}
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={status.HTTP_200_OK: 'OK', status.HTTP_401_UNAUTHORIZED: 'Unauthorized'}
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Account is disabled"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"message": "Invalid input"}, status=status.HTTP_401_UNAUTHORIZED)