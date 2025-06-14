from django import forms
<<<<<<< HEAD
from .models import Exam, Subject, Topic, Pet
from .models import DailyNote
=======
from .models import Exam, Subject, Topic
from .models import DailyNote, Pet

class ChangePet(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['pet', 'user']
>>>>>>> 55da34f (commit)

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

class DailyNoteForm(forms.ModelForm):
    class Meta:
        model = DailyNote
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 10, 'cols': 30}),
<<<<<<< HEAD
        }

class ChangePet(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['pet', 'user']
=======
        }
>>>>>>> 55da34f (commit)
