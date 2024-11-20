from rest_framework import viewsets
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Tutor
from .serializers import TutorSerializer
from students.models import Student
from friend_requests.models import FriendRequest  # Import the FriendRequest model
from django.contrib.auth.decorators import login_required


class TutorViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for managing Tutor CRUD operations.
    """
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer


def tutor_login(request):
    """
    Handles tutor login functionality.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            tutor = Tutor.objects.get(username=username)
            if tutor.password == password:  # Simple password check
                # Store tutor's details in session
                request.session['user_role'] = 'Tutor'
                request.session['username'] = tutor.username
                messages.success(request, 'Login successful.')
                return redirect('tutors:tutors_dashboard')  # Correct namespace usage
            else:
                messages.error(request, 'Invalid username or password.')
        except Tutor.DoesNotExist:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def tutor_logout(request):
    """
    Logs out the tutor and redirects to the home page.
    """
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('/')


def tutors_list(request):
    """
    Renders a list of all tutors.
    """
    query = request.GET.get('query', '')  # Get the search query from the request
    if query:
        tutors = Tutor.objects.filter(
            first_name__icontains=query) | Tutor.objects.filter(last_name__icontains=query) | Tutor.objects.filter(subject__icontains=query)
    else:
        tutors = Tutor.objects.all()

    return render(request, 'tutors_list.html', {'tutors': tutors, 'query': query})


def tutors_dashboard(request):
    # Fetch the students data (assuming Student is a model)
    students = Student.objects.all()  # Fetch all students, adjust this as needed
    
    # Passing students data to the template
    context = {
        'students': students,
    }
    return render(request, 'tutors/tutors_dashboard.html', context)


def send_friend_request(request, student_id):
    """
    Sends a friend request from a student to a tutor.
    """
    student = get_object_or_404(Student, id=student_id)
    tutor = get_object_or_404(Tutor, username=request.session.get('username'))

    # Check if a friend request already exists
    if FriendRequest.objects.filter(student=student, tutor=tutor).exists():
        messages.error(request, "Friend request already sent.")
    else:
        # Create a new friend request
        FriendRequest.objects.create(student=student, tutor=tutor, status='Pending')
        messages.success(request, "Friend request sent successfully.")

    return redirect('tutors:tutors_dashboard')


@login_required
def handle_friend_request(request, request_id, action):
    """
    Handles friend request actions (accept/decline).
    """
    friend_request = get_object_or_404(FriendRequest, id=request_id)

    if action == 'accept':
        friend_request.status = 'Accepted'
        friend_request.save()
        messages.success(request, f"You are now connected with {friend_request.student.fullname}.")
    elif action == 'decline':
        friend_request.status = 'Declined'
        friend_request.save()
        messages.success(request, "Friend request declined.")
    else:
        messages.error(request, "Invalid action.")

    return redirect('tutors:tutors_dashboard')
