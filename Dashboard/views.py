from django.shortcuts import render
from kinde_sdk.kinde_api_client import GrantType, KindeApiClient # Import Kinde's authentication checker

# Create your views here.
def Dashboard(request):
     if request.session.get('user_id'):  # Check if user is authenticated via session
        return render(request, 'Dashboard/index.html')
     else:
        return render(request, 'Homepage/index.html')


