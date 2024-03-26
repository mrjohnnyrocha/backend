from django.contrib.auth.hashers import make_password
from app.models import CustomUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class UserService:
    @staticmethod
    def create_user(email, username, password, **extra_fields):
        """
        Create and return a user with an email, username, and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        
        email = CustomUser.objects.normalize_email(email)
        user = CustomUser(
            email=email,
            username=username,
            password=make_password(password),
            **extra_fields
        )
        user.full_clean()
        user.save()
        return user

    @staticmethod
    def update_user(user_uuid, **data):
        """
        Update user details
        """
        try:
            user = CustomUser.objects.get(uuid=user_uuid)
            for field, value in data.items():
                setattr(user, field, value)
            user.full_clean()
            user.save()
            return user
        except CustomUser.DoesNotExist:
            raise ValidationError(_('User does not exist'))

    @staticmethod
    def delete_user(user_uuid):
        """
        Delete a user.
        """
        try:
            user = CustomUser.objects.get(uuid=user_uuid)
            user.delete()
            return True
        except CustomUser.DoesNotExist:
            raise ValidationError(_('User does not exist'))

    @staticmethod
    def get_user_by_email(email):
        """
        Retrieve a user by email.
        """
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise ValidationError(_('User does not exist'))
