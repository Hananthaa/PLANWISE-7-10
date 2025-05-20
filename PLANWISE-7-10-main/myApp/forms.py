from django import forms
from .models import Exam, Subject, Topic

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['subject', 'exam_date', 'mark']  # Add 'mark'

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subject', 'exam_date']

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content']