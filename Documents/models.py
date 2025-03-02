from django.db import models
from django.conf import settings
import uuid

class Briefcase(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def document_upload_path(instance, filename):
        return f"documents/{instance.briefcase.user.id}/{instance.briefcase.id}/{filename}"

class Document(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # 🔥 Allow NULL temporarily
    briefcase = models.ForeignKey(Briefcase, on_delete=models.CASCADE, related_name="documents")
    file = models.FileField(upload_to=document_upload_path)
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processing_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], default='pending')

    def __str__(self):
        return self.filename
    
class Question(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    briefcase = models.ForeignKey(Briefcase, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()

    def __str__(self):
        return self.text[:50]  # Truncate long questions for readability
    
class ProcessingJob(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="processing_jobs")
    status = models.CharField(max_length=20, choices=[
        ('queued', 'Queued'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], default='queued')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Job {self.id} - {self.status}"

class AnswerSet(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    briefcase = models.ForeignKey(Briefcase, on_delete=models.CASCADE, related_name="answersets")
    json_data = models.JSONField()  # Stores AI-extracted responses
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answers for {self.briefcase.title}"