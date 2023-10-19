from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .forms import UserRegistrationForm
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    referral_email = serializers.CharField(source='userprofile.referral_email', read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'referral_email']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    referral_email = serializers.EmailField(allow_blank=True, required=False)

    def create(self, validated_data):
        user_data = {
            'username': validated_data['username'],
            'email': validated_data['email'],
            'password1': validated_data['password1'],
            'password2': validated_data['password2']
        }
        referral_email = validated_data.get('referral_email')

        form = UserRegistrationForm(user_data)
        if form.is_valid():
            user = form.save()
            if referral_email:
                user_profile = UserProfile.objects.get(user=user)
                user_profile.referral_email = referral_email
                user_profile.save()
            return user
        else:
            raise serializers.ValidationError(form.errors)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)