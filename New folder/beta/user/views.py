from django.shortcuts import redirect, reverse
from django.http import HttpResponse
import requests
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

def apple_authorization(request):
    authorization_url = "https://appleid.apple.com/auth/authorize"
    redirect_uri = request.build_absolute_uri(reverse('https://jampass.onrender.com/')) 
    client_id = settings.APPLE_CLIENT_ID
    scope = "openid email " 
    
    return redirect(f"{authorization_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}")

def apple_callback(request):
    authorization_code = request.GET.get('code')
    token_endpoint = 'https://appleid.apple.com/auth/token'
    client_id = settings.APPLE_CLIENT_ID
    client_secret = settings.APPLE_CLIENT_SECRET
    redirect_uri = request.build_absolute_uri(reverse('apple_callback'))
    
    token_response = requests.post(token_endpoint, {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': authorization_code,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
    })
    
    if token_response.status_code == 200:
        tokens = token_response.json()
        access_token = tokens['access_token']
        id_token = tokens['id_token']
        
        
        decoded_token = validate_token(id_token)
        
        user_id = decoded_token['sub']  
        user_email = decoded_token['email'] 
        user, created = User.objects.get_or_create(username=user_email, email=user_email)
        
        return HttpResponse('Authorization successful')
    else: 
        return HttpResponse('Authorization failed')

def validate_token(token):
    try:
        decoded_token = jwt.decode(token, settings.APPLE_PUBLIC_KEY, algorithms=['RS256'])
        exp_timestamp = decoded_token.get('exp')
        if exp_timestamp is not None and datetime.utcfromtimestamp(exp_timestamp) < datetime.utcnow():
            raise PermissionDenied("Token has expired")
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise PermissionDenied("Token has expired")
    except jwt.InvalidTokenError:
        raise PermissionDenied("Invalid token")
