import jwt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


import mrjohnnyrocha.settings

from app.models import Conversation, CustomUser
from app.serializers import ConversationSerializer, UserSerializer
from app.forms import (
    LoginForm,
    ForgotPasswordForm,
    UserRegistrationForm,
    UserSettingsForm,
)
from app.services.user import UserService


class UserAPI(APIView):
    user_service = UserService()

    def get(self, request, format=None):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            created_user = self.user_service.register_user(
                data["username"], data["email"], data["password"]
            )
            return Response(
                UserSerializer(created_user).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPI(APIView):
    #    @ratelimit(key="ip", rate="5/m", method="POST", block=True)
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            serializer = TokenObtainPairSerializer(data=request.data)
            refresh = RefreshToken.for_user(user)
            if serializer.is_valid():
                        return Response(serializer.validated_data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                    'refresh': str(refresh) + '/',
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data # Serialize user data
                }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})



class UserSignupAPI(APIView):
    # @ratelimit(key="ip", rate="5/m", method="POST", block=True)
    def post(self, request):
        username = request.data.get("email")
        password = request.data.get("password")
        if not username or not password:
            return Response(
                {"error": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user, created = CustomUser.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            user.save()
            serializer = TokenObtainPairSerializer(data=request.data)
            if serializer.is_valid():
                return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
            return Response(
                {"error": f"Something went wrong: {serializer.errors}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            return Response(
                {"error": "User with this email already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get(self, request):
        form = UserRegistrationForm()
        return render(request, "register.html", {"form": form})


class ForgotPasswordAPI(View):
    # @ratelimit(key="ip", rate="5/m", method="POST", block=True)
    def post(self, request):
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            try:
                user = CustomUser.objects.get(email=form.cleaned_data["email"])
                # Rest of the logic...
            except CustomUser.DoesNotExist:
                pass
                # Handle non-existent user case
        else:
            form = ForgotPasswordForm()
        return render(request, "forgot_password.html", {"form": form})

    def get(self, request):
        form = ForgotPasswordForm()
        return render(request, "forgot_password.html", {"form": form})


class UserLogoutAPI(APIView):
    def post(self, request):
        logout(request)
        return Response({"success": "User signed out successfully"})

@method_decorator(login_required, name="dispatch")
# @method_decorator(ratelimit(key="ip", rate="5/m", method="POST", block=True), name='dispatch')
class UserProfileAPI(APIView):
    def post(self, request):
        form = UserSettingsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("user_settings_success")
        return render(request, "user_settings.html", {"form": form})

    def get(self, request):
        form = UserSettingsForm(instance=request.user)
        return render(request, "user_settings.html", {"form": form})


class UserConversationsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        conversations = Conversation.objects.filter(members=request.user)
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)


class SessionValidateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        authorization_header = request.headers.get("Authorization")
        if authorization_header is None or not authorization_header.startswith(
            "Bearer "
        ):
            return Response(
                {"error": "No token provided"}, status=status.HTTP_401_UNAUTHORIZED
            )

        token = authorization_header.split("Bearer ")[1].strip()
        try:

            payload = jwt.decode(token, DJANGO_SECRET_KEY, algorithms=["HS256"])
            user = CustomUser.objects.get(id=payload["user_id"])
            return Response(
                {"user": UserSerializer(user).data}, status=status.HTTP_200_OK
            )
        except jwt.ExpiredSignatureError:
            return Response(
                {"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED
            )
        except jwt.DecodeError:
            return Response(
                {"error": "Error decoding token"}, status=status.HTTP_401_UNAUTHORIZED
            )
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
