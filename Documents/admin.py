from django.contrib import admin
from .models import Briefcase, Document, Question, AnswerSet, ProcessingJob

@admin.register(Briefcase)
class BriefcaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('filename', 'briefcase', 'uploaded_at', 'processing_status')
    list_filter = ('processing_status',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('briefcase', 'text')

@admin.register(AnswerSet)
class AnswerSetAdmin(admin.ModelAdmin):
    list_display = ('briefcase', 'created_at')

@admin.register(ProcessingJob)
class ProcessingJobAdmin(admin.ModelAdmin):
    list_display = ('document', 'status', 'created_at', 'completed_at')
