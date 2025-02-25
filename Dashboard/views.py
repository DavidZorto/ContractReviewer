from django.shortcuts import render, get_object_or_404, redirect
from kinde_sdk.kinde_api_client import GrantType, KindeApiClient # Import Kinde's authentication checker
from django.contrib.auth.decorators import login_required
from Documents.models import Briefcase, Document, Question, ProcessingJob, AnswerSet
from django.contrib import messages
from Documents.forms import BriefcaseForm, DocumentForm, QuestionForm, ProcessingJobForm, AnswerSetForm  # Assuming you have forms for each model
import uuid
from django.http import HttpResponse
from django.template.loader import render_to_string

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



# Briefcase CRUD
@login_required  #  Protect this view so only logged-in users can access it
def Briefcases(request):
    briefcases = Briefcase.objects.filter(user=request.user).order_by("-created_at") 
    return render(request, "Dashboard/briefcases.html", {"briefcases": briefcases})


@login_required
def create_briefcase(request):
    if request.method == 'POST':
        form = BriefcaseForm(request.POST)
        if form.is_valid():
            briefcase = form.save(commit=False)
            briefcase.user = request.user  # Associate with logged-in user
            briefcase.save()
            messages.success(request, "Briefcase created successfully.")

            # If HTMX is making the request, return only the updated list
            if 'HX-Request' in request.headers:
                briefcases = Briefcase.objects.filter(user=request.user)
                updated_briefcases_html = render_to_string('Dashboard/briefcases.html', {'briefcases': briefcases}, request)
                return HttpResponse(updated_briefcases_html)

            return redirect('Dashboard:briefcases')  # Fallback for non-HTMX users

    else:
        form = BriefcaseForm()

    # Render only the form for HTMX
    form_html = render_to_string('Dashboard/partials/briefcase_form.html', {'form': form}, request)
    return HttpResponse(form_html)


@login_required
def read_briefcase(request, briefcase_id):
    briefcase = get_object_or_404(Briefcase, id=briefcase_id, user=request.user)
    return render(request, 'Dashboard/briefcase_detail.html', {'briefcase': briefcase})

@login_required
def update_briefcase(request, briefcase_id):
    briefcase = get_object_or_404(Briefcase, id=briefcase_id, user=request.user)
    if request.method == 'POST':
        form = BriefcaseForm(request.POST, instance=briefcase)
        if form.is_valid():
            form.save()
            messages.success(request, "Briefcase updated successfully.")
            return redirect('Dashboard:briefcases')
    else:
        form = BriefcaseForm(instance=briefcase)
    return render(request, 'Dashboard/briefcase_form.html', {'form': form})


@login_required
def delete_briefcase(request, id):
    briefcase = get_object_or_404(Briefcase, id=id, user=request.user)
    briefcase.delete()
    messages.success(request, "Briefcase deleted successfully.")
    return redirect('Dashboard:briefcases')

















@login_required  # 🔐 Require login to access documents
def Documents(request):
    documents = Document.objects.filter(user=request.user)  # 🔥 Show only the user's documents
    return render(request, 'Dashboard/documents.html', {'documents': documents})