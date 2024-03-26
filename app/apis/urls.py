from django.urls import path
from . import welcome_page, conversation, user, privacy_policy, message
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "api"

urlpatterns = [
    path("welcome_page/", welcome_page.WelcomePageAPI.as_view(), name="welcome_page"),
    path("conversation/", conversation.ConversationAPI.as_view(), name="conversation"),
    path("conversation/<str:name>/", conversation.ConversationAPI.as_view(), name="conversation_by_name"),
    path("user/", user.UserAPI.as_view(), name="user"),
    path(
        "privacy_policy/",
        privacy_policy.PrivacyPolicyAPI.as_view(),
        name="privacy_policy",
    ),
    path("message/", message.MessageAPI.as_view(), name="message"),
    path("auth/signin/", user.UserLoginAPI.as_view(), name="signin"),
    path("auth/signout/", user.UserLogoutAPI.as_view(), name="signout"),
    path("auth/signup/", user.UserSignupAPI.as_view(), name="signup"),
    path(
        "session/validate",
        user.SessionValidateAPI.as_view(),
        name="session_validate",
    ),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("user/profile/", user.UserProfileAPI.as_view(), name="UserProfileAPI"),
]
