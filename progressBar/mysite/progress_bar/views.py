from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import ExamForm
from .models import Exam

'''
# Create your views here.
def test(request):
    #template = loader.get_template('test.html')
    #return HttpResponse(template.render())
    return render(request, 'assign&exambox.html')
'''

def test(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exam_success')  # Redirect to a success page
    else:
        form = ExamForm()
    exams = Exam.objects.all()  # Retrieve all saved exams
    return render(request, 'assign&exambox.html', {'form': form, 'exams': exams})

def exam_success(request):
    return render(request, 'exam_success.html')

def display_exams(request):
    exams = Exam.objects.all()  # Retrieve all Exam objects from the database
    return render(request, 'display_exams.html', {'exams': exams})

def delete_exam(request, exam_id):
    if request.method == 'POST':
        exam = get_object_or_404(Exam, pk=exam_id)
        exam.delete()
    return redirect('test')