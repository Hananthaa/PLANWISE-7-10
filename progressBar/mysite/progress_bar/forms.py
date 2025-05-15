from django import forms
from .models import Exam

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['subject', 'exam_date']
        widgets = {
            'exam_date': forms.DateInput(attrs={'type': 'date'})
        }