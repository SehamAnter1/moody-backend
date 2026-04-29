import os

from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
import requests
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# Create your views here.
User = get_user_model()
from  django.shortcuts import redirect
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
def get_redirect_uri(request):
    return request.build_absolute_uri("/api/auth/google/callback/")
@csrf_exempt
def google_login(request):

    url = url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={get_redirect_uri(request)}"
        "&response_type=code"
        "&scope=openid email profile"
    )
    return redirect(url)
@csrf_exempt
def google_callback(request):
    code = request.GET.get('code')
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": get_redirect_uri(request),
        "grant_type": "authorization_code",
    }
    token_res = requests.post(token_url, data=data)
    token_data = token_res.json()
    if "access_token" not in token_data:
        return redirect("http://localhost:3000/login?error=google_failed")

    print("token_data",token_data)
    user_info = requests.get("https://www.googleapis.com/oauth2/v2/userinfo", headers={"Authorization": f"Bearer {token_data['access_token']}"}).json()
    email = user_info['email']
    user, _ = User.objects.get_or_create(email=email, defaults={"username": email.split('@')[0],})
    refresh = RefreshToken.for_user(user)
    response = redirect("http://localhost:3000/")
    response.set_cookie(
            "access_token",
            str(refresh.access_token),
            httponly=True,
            secure=False,  # True in production (HTTPS)
            samesite="Lax",
        )
    response.set_cookie(
            "refresh_token",
            str(refresh),
            httponly=True,
            secure=False,  # True in production (HTTPS)
            samesite="Lax",
        )
    return response