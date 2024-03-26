from rest_framework import serializers
from django_countries.serializer_fields import CountryField

from app.models.user import CustomUser

class UserSerializer(serializers.ModelSerializer):
    country = CountryField(country_dict=True)  # This will represent the country with its code and name.
    id = serializers.UUIDField(format='hex_verbose')
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'country', 'first_name', 'last_name', 'is_active', 'is_staff', 'profile_picture', 'bio', 'phone_number', 'date_of_birth']
        extra_kwargs = {
            'profile_picture': {'required': False},
            'bio': {'required': False},
            'phone_number': {'required': False},
            'date_of_birth': {'required': False},
        }
