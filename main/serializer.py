from rest_framework import serializers
from .models import User
import random

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "phone_number", "password"]

    def create(self, validated_data):
        code = str(random.randint(100000, 999999))
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            phone_number=validated_data["phone_number"],
            password=validated_data["password"],
            verification_code=code,
            is_verified=False
        )
        from django.core.mail import send_mail
        send_mail(
            "Tasdiqlash kodi",
            f"Sizning tasdiqlash kodingiz: {code}",
            "yourgmail@example.com",
            [validated_data["email"]],
            fail_silently=False,
        )
        return user


class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs["email"], verification_code=attrs["code"])
        except User.DoesNotExist:
            raise serializers.ValidationError("Kod noto‘g‘ri!")
        user.is_verified = True
        user.verification_code = None
        user.save()
        return attrs

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "phone_number"]

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        instance.save()
        return instance

class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError("Bunday email topilmadi!")

        import random
        code = str(random.randint(100000, 999999))
        user.verification_code = code
        user.save()

        from django.core.mail import send_mail
        send_mail(
            "Parolni tiklash kodi",
            f"Sizning reset kodingiz: {code}",
            "yourgmail@example.com",
            [attrs["email"]],
            fail_silently=False,
        )

        return attrs


class ResetPasswordConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs["email"], verification_code=attrs["code"])
        except User.DoesNotExist:
            raise serializers.ValidationError("Kod xato yoki email topilmadi!")

        user.set_password(attrs["new_password"])
        user.verification_code = None
        user.save()
        return attrs

