# Subject/views.py
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Subject
from .forms import SubjectForm

def subject_management(request):
    form = SubjectForm()
    subjects = Subject.objects.all()
    return render(request, 'subject_management.html', {'form': form, 'subjects': subjects})

def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save()
            return JsonResponse({'id': subject.subject_id, 'name': subject.subject_name})
    return JsonResponse({'error': 'Invalid data'}, status=400)

def update_subject(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            subject = form.save()
            return JsonResponse({'id': subject.subject_id, 'name': subject.subject_name})
    return JsonResponse({'error': 'Invalid data'}, status=400)


def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    subject.delete()
    return JsonResponse({'id': subject_id})
