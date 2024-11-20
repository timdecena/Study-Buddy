from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import FriendRequest
from tutors.models import Tutor
from students.models import Student


def send_friend_request(request, tutor_id):
    # Check if the user is authenticated and logged in as a student (using session data)
    if not request.session.get('user_role') == 'student':  # Check if the user is logged in as a student
        messages.error(request, "You must be logged in as a student to send a friend request.")
        return redirect('students:login')  # Redirect to the login page
    
    # Retrieve the student and tutor
    student = get_object_or_404(Student, username=request.session['username'])  # Get logged-in student by username
    tutor = get_object_or_404(Tutor, id=tutor_id)  # Get the tutor by ID

    # Create the friend request
    FriendRequest.objects.create(student=student, tutor=tutor)
    messages.success(request, "Friend request sent!")
    
    return redirect('tutors:tutors_list')  # Redirect to the tutors list or another relevant page

def view_friend_requests(request):
    tutor = get_object_or_404(Tutor, username=request.user.username)
    friend_requests = FriendRequest.objects.filter(tutor=tutor, status="Pending")
    return render(request, 'tutors_dashboard.html', {'friend_requests': friend_requests})

def handle_friend_request(request, request_id, action):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if action == 'accept':
        friend_request.status = 'Accepted'
    elif action == 'decline':
        friend_request.status = 'Declined'
    friend_request.save()
    return redirect('tutors_dashboard')




