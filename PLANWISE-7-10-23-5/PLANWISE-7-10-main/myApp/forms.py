from django import forms
from .models import Exam, Subject, Topic, Pet

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['subject', 'exam_date', 'mark']  # Add 'mark'

#tracker
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subject', 'exam_date']

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title']

class ChangePet(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['pet', 'user']
