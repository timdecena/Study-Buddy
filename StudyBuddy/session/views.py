# session/views.py
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Session
from .forms import SessionForm
from django.views.decorators.csrf import csrf_exempt

def session_management(request):
    form = SessionForm()
    sessions = Session.objects.all()
    return render(request, 'session_management.html', {'form': form, 'sessions': sessions})

@csrf_exempt
def add_session(request):
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.save()
            return JsonResponse({
                'id': session.session_id,
                'name': session.session_name,
                'schedule_date': session.schedule_date.strftime('%Y-%m-%d'),
                'time_start': session.time_start,
                'tutor': session.tutor.last_name,
                'student': session.student.fullname,
                'course': session.course.course_name
            })
    return JsonResponse({'error': 'Invalid data'}, status=400)

@csrf_exempt
def update_session(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    if request.method == 'POST':
        form = SessionForm(request.POST, instance=session)
        if form.is_valid():
            session = form.save()
            return JsonResponse({
                'id': session.session_id,
                'name': session.session_name,
                'schedule_date': session.schedule_date.strftime('%Y-%m-%d'),
                'time_start': session.time_start,
                'tutor': session.tutor.last_name,
                'student': session.student.fullname,
                'course': session.course.course_name
            })
    return JsonResponse({'error': 'Invalid data'}, status=400)

@csrf_exempt
def delete_session(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    session.delete()
    return JsonResponse({'id': session_id})
