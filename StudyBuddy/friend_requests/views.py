from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import FriendRequest
from students.models import Student
from tutors.models import Tutor

def send_friend_request(request, receiver_type, receiver_id):
    sender_student = None
    sender_tutor = None

    # Determine sender based on logged-in user role
    if request.session.get('user_role') == 'student':
        sender_student = Student.objects.get(username=request.session['username'])
    elif request.session.get('user_role') == 'tutor':
        sender_tutor = Tutor.objects.get(username=request.session['username'])

    # Determine receiver based on type
    if receiver_type == 'student':
        receiver_student = get_object_or_404(Student, pk=receiver_id)
        friend_request = FriendRequest(sender_student=sender_student, receiver_student=receiver_student)
    elif receiver_type == 'tutor':
        receiver_tutor = get_object_or_404(Tutor, pk=receiver_id)
        friend_request = FriendRequest(sender_tutor=sender_tutor, receiver_tutor=receiver_tutor)

    # Save the friend request
    friend_request.save()
    messages.success(request, 'Friend request sent successfully!')
    return redirect('students:student_homepage' if sender_student else 'tutors:tutors_dashboard')

def handle_friend_request(request, request_id, action):
    friend_request = get_object_or_404(FriendRequest, pk=request_id)

    if action == 'accept':
        friend_request.status = 'accepted'
        messages.success(request, 'Friend request accepted!')
    elif action == 'decline':
        friend_request.status = 'declined'
        messages.info(request, 'Friend request declined.')

    friend_request.save()
    return redirect('students:student_homepage' if request.session['user_role'] == 'student' else 'tutors:tutors_dashboard')

def list_friend_requests(request):
    if request.session.get('user_role') == 'student':
        user = Student.objects.get(username=request.session['username'])
        received_requests = FriendRequest.objects.filter(receiver_student=user, status='pending')
    elif request.session.get('user_role') == 'tutor':
        user = Tutor.objects.get(username=request.session['username'])
        received_requests = FriendRequest.objects.filter(receiver_tutor=user, status='pending')

    return render(request, 'friend_requests/list_requests.html', {'received_requests': received_requests})
