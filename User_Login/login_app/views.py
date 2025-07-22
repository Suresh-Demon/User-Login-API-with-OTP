from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, OTP
from .utils import generate_otp, generate_token
from django.utils import timezone
from datetime import timedelta

@api_view(['POST'])
def register(request):
    email = request.data.get('email')
    if not email:
        return Response({"error": "Email required"})
    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already registered"})
    User.objects.create(email=email)
    return Response({"message": "Registration successful.Please verify your email."})

@api_view(['POST'])
def request_otp(request):
    email = request.data.get('email')
    user = User.objects.filter(email=email).first()
    if not user:
        return Response({"error": "User not found"})
    code = generate_otp()
    OTP.objects.create(user=user, otp_code=code)
    print(f"OTP for {email}: {code}")  
    return Response({"message": "OTP sent to your email"})

@api_view(['POST'])
def verify_otp(request):
    email = request.data.get('email')           
    otp = request.data.get('otp')               
    user = User.objects.filter(email=email).first()  
    if not user:
        return Response({"error": "User not found"})  
    otp_obj = OTP.objects.filter(user=user, otp_code=otp).order_by('-created_at').first()
    if otp_obj and timezone.now() - otp_obj.created_at < timedelta(minutes=5):
        user.is_verified = True       
        user.save()
        token = generate_token(user)  
        return Response({"message": "Login successful ", "token": token})  
    return Response({"error": "Invalid or expired OTP"})

