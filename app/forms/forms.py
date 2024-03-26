from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from app.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields 

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password', 'country')

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'profile_picture', 'bio', 'phone_number', 'date_of_birth')
