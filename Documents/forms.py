from django import forms
from .models import Briefcase, Document, Question, ProcessingJob, AnswerSet

class BriefcaseForm(forms.ModelForm):
    class Meta:
        model = Briefcase
        fields = ['title']  # Add other fields as necessary

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file', 'filename', 'briefcase']  # Include fields relevant to Document

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'briefcase']  # Include fields relevant to Question

class ProcessingJobForm(forms.ModelForm):
    class Meta:
        model = ProcessingJob
        fields = ['document', 'status']  # Include fields relevant to ProcessingJob

class AnswerSetForm(forms.ModelForm):
    class Meta:
        model = AnswerSet
        fields = ['json_data', 'briefcase']  # Include fields relevant to AnswerSet