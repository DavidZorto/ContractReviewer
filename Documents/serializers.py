from rest_framework import serializers
from .models import Briefcase, Document, Question, AnswerSet, ProcessingJob

class BriefcaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Briefcase
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class AnswerSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerSet
        fields = '__all__'

class ProcessingJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessingJob
        fields = '__all__'
