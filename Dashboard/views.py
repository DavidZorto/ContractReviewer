from django.shortcuts import render
from kinde_sdk.kinde_api_client import GrantType, KindeApiClient # Import Kinde's authentication checker
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Documents.models import Briefcase, Document, Question, ProcessingJob, AnswerSet
from django.core.paginator import Paginator



# Create your views here.
def render_template(request, authenticated_template, unauthenticated_template):
    if request.session.get('user_id'):  # Check if user is authenticated via session
        return render(request, authenticated_template)
    else:
        return render(request, unauthenticated_template)

def Dashboard(request):
    return render_template(request, 'Dashboard/index.html', 'Homepage/index.html')

def Dashboard_home(request):
    return render_template(request, 'Dashboard/Home.html', 'Homepage/index.html')

def Processing_jobs(request):
    return render_template(request, 'Dashboard/processing_jobs.html', 'Homepage/index.html')  # Main section for Processing Jobs

def Answers(request):
    return render_template(request, 'Dashboard/answers.html', 'Homepage/index.html')  # Main section for Answers


@login_required  # 🔐 Protect this view so only logged-in users can access it
def Briefcases(request):
    page_number = request.GET.get("page", 1)  # Get page number from request
    briefcases_list = Briefcase.objects.filter(user=request.user).order_by("-created_at")  # Only user's briefcases
    paginator = Paginator(briefcases_list, 10000)  # Show 5 briefcases per page

    briefcases = paginator.get_page(page_number)

    # If HTMX request, return only the list items (partial)
    if request.htmx:
        return render(request, "Dashboard/briefcases.html", {"briefcases": briefcases})

    return render(request, "Dashboard/briefcases.html", {"briefcases": briefcases})

@login_required  # 🔐 Require login to access documents
def Documents(request):
    documents = Document.objects.filter(user=request.user)  # 🔥 Show only the user's documents
    return render(request, 'Dashboard/documents.html', {'documents': documents})