from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import User
from .serializer import SignupSerializer, VerifySerializer , ProfileUpdateSerializer , ResetPasswordConfirmSerializer , ResetPasswordRequestSerializer

class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]


class VerifyView(generics.GenericAPIView):
    serializer_class = VerifySerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Muvaffaqiyatli tasdiqlandi!"})

class ProfileView(generics.RetrieveAPIView):
    serializer_class = SignupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class ProfileUpdateView(generics.UpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ResetPasswordRequestView(generics.GenericAPIView):
    serializer_class = ResetPasswordRequestSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Reset kodi emailingizga yuborildi"})


class ResetPasswordConfirmView(generics.GenericAPIView):
    serializer_class = ResetPasswordConfirmSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Parolingiz yangilandi"})

