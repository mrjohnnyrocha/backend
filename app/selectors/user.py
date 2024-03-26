from app.models import CustomUser
from app.services import UserService

class UserSelector:
    def get_default_user(self):
        try:
            return CustomUser.objects.get(email="default@example.com")
        except CustomUser.DoesNotExist:
             user_service = UserService()
             user = user_service.register_user(username="default", email="default@example.com", password="qwer1234")
             return user
    
    def get_user_by_email(email: str):
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None

    def get(self, uuid):
        if uuid is not None:
            return CustomUser.objects.get(uuid=uuid)
        return None 
