import random

from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Student
from .serializers import StudentSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

class GetTokenView(TokenObtainPairView):
    pass

class SendOTPView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        if not phone:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a random 6-digit OTP
        otp = random.randint(100000, 999999)

        # Cache the OTP with the key as phone_otp for 5 minutes
        cache.set(f'{phone}_otp', otp, timeout=300)

        # Simulate sending the OTP (you would integrate with an SMS service here)
        # For now, just print or return the OTP for testing purposes
        print(f"Sending OTP {otp} to phone {phone}")
        return Response({'message': f'OTP sent successfully {otp}'}, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        otp = request.data.get('otp')

        if not phone or not otp:
            return Response({'error': 'Phone number and OTP are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the cached OTP
        cached_otp = cache.get(f'{phone}_otp')

        if cached_otp is None:
            return Response({'error': 'OTP expired or not found'}, status=status.HTTP_400_BAD_REQUEST)

        if str(cached_otp) == str(otp):
            # OTP is valid, retrieve the student based on the phone number
            cache.delete(cached_otp)
            try:
                student = Student.objects.get(phone=phone)  # Assuming phone is a field in the Student model
            except Student.DoesNotExist:
                return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

            # Generate JWT tokens for the student
            refresh = RefreshToken.for_user(student)  # This assumes the Student model is linked to a user or has JWT support

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

class AddStudentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetStudentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
