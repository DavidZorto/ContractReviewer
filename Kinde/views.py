from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
# Import the Kinde SDK, dotenv and a few std lib modules
import os, base64
from kinde_sdk.kinde_api_client import GrantType, KindeApiClient
from dotenv import load_dotenv

import ssl
import requests

from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login

User = get_user_model()



# Disable SSL verification globally (TEMPORARY)
ssl._create_default_https_context = ssl._create_unverified_context


# Call load_dotenv so we can access values from the .env file
load_dotenv()

# For now, we'll just use a dictionary to hold a bunch of clients for each
# user in memory
user_clients = {}

# A few helper functions to manage
# the data coming back from Kinde
def __get_empty_context():
    return {
        "authenticated": False,
        "user_first_name": "",
        "user_last_name": "",
    }

def __get_user_context(user_id):
    context = __get_empty_context()

    user_client = user_clients.get(user_id)

    if user_client is not None:
        is_user_authenticated = user_client.get('kinde_client').is_authenticated()
        user_last_name = user_client.get('user_last_name')
        user_first_name = user_client.get('user_first_name')

        context = {
            "authenticated": is_user_authenticated,
            "user_first_name": user_first_name,
            "user_last_name": user_last_name,
            "user_full_name": user_first_name + ' ' + user_last_name,
            "user_initials": user_first_name[0] + f"{user_last_name[0] if user_last_name is not None else user_first_name[1]}"
        }

    return context

def __get_new_kinde_client():
    domain = os.getenv("KINDE_ISSUER_URL")
    callback_url = f"{os.getenv('SITE_DOMAIN')}/Kinde/callback"
    return KindeApiClient(
        domain=domain,
        callback_url=callback_url,
        client_id=os.getenv("KINDE_CLIENT_ID"),
        client_secret=os.getenv("KINDE_CLIENT_SECRET"),
        grant_type=GrantType.AUTHORIZATION_CODE,
    )


# What gets run when you sign in
def login(request):
    context = __get_empty_context()

    # Check if User is not signed in
    if request.session.get('user_id') is None:
        kinde_client = __get_new_kinde_client()
        return redirect(kinde_client.get_login_url())
    else:
        user_id = request.session.get('user_id')
        context = __get_user_context(user_id)
        return render(request, "Kinde/dashboard.html", context)

# What gets run when you register
def register(request):
    # Check if User is not signed in
    if request.session.get('user_id') is None:
        kinde_client = __get_new_kinde_client()
        return redirect(kinde_client.get_register_url())
    else:
        user_id = request.session.get('user_id')
        context = __get_user_context(user_id)
        return render(request, "kinde/dashboard.html", context)

# When your user is done authenticating in Kinde
# Kinde calls this route back
def callback(request):

    context = __get_empty_context()
    #Check If the User Is Already Logged In
    if request.session.get('user_id') is None:

        kinde_client = __get_new_kinde_client()
        kinde_client.fetch_token(authorization_response=request.build_absolute_uri())
        user_details = kinde_client.get_user_details()
        
        user_id = user_details['id']
        email = user_details.get('email', '')


        request.session['user_id'] = user_id

        user_clients[user_id] = {
            "kinde_client": kinde_client,
            "authenticated": True,
            "user_first_name": user_details.get('given_name', ''),  # ✅ Avoid KeyError
            "user_last_name": user_details.get('family_name', ''),  # ✅ Avoid KeyError
        }

        # Get or create user
        user, created = User.objects.get_or_create(
            email=email,  # Assuming email is unique
            defaults={'username': email}  # Set default username as email
        )
        
        auth_login(request, user)

        return redirect('Dashboard:index')

    else:
        user_id = request.session.get('user_id')
        context = __get_user_context(user_id)

    return redirect('Dashboard:index')

# What gets run when you logout
def logout(request):
    from django.conf import settings
    index_path = request.build_absolute_uri('/')
    user_id = request.session.get('user_id')
    
    request.session.flush()
    
    if user_id and user_id in user_clients:
        kinde_client = user_clients[user_id].get('kinde_client')
        if kinde_client:
            user_clients.pop(user_id)
            return redirect(kinde_client.logout(redirect_to=index_path))
    
    return redirect(index_path)

