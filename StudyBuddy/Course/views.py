# Course/views.py
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Course
from .forms import CourseForm

def course_management(request):
    form = CourseForm()
    courses = Course.objects.all()
    return render(request, 'course_management.html', {'form': form, 'courses': courses})

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            return JsonResponse({'id': course.course_id, 'name': course.course_name, 'code': course.course_code, 'description': course.description})
    return JsonResponse({'error': 'Invalid data'}, status=400)

def update_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save()
            return JsonResponse({'id': course.course_id, 'name': course.course_name, 'code': course.course_code, 'description': course.description})
    return JsonResponse({'error': 'Invalid data'}, status=400)

def delete_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    course.delete()
    return JsonResponse({'id': course_id})
