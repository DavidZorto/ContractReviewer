from django.shortcuts import render, redirect
from kinde_sdk.kinde_api_client import GrantType, KindeApiClient # Import Kinde's authentication checker

# Create your views here.
def homepage(request):
    if request.session.get('user_id'):
        return redirect('Dashboard:index')
    return render(request, 'Homepage/index.html')


