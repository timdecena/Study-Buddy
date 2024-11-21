from rest_framework import viewsets

from friend_requests.models import FriendRequest
from .models import Tutor
from .serializers import TutorSerializer
from django.shortcuts import get_object_or_404, render, redirect
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




def accept_friend_request(request, id):
    # Get the friend request by ID
    friend_request = get_object_or_404(FriendRequest, id=id)

    # Change the status to 'accepted'
    friend_request.status = 'accepted'
    friend_request.save()

    messages.success(request, 'Friend request accepted.')
    return redirect('tutors:tutors_dashboard')

def reject_friend_request(request, id):
    # Get the friend request by ID
    friend_request = get_object_or_404(FriendRequest, id=id)

    # Change the status to 'rejected'
    friend_request.status = 'rejected'
    friend_request.save()

    messages.success(request, 'Friend request rejected.')
    return redirect('tutors:tutors_dashboard')




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
    username = request.session.get('username')
    if not username:
        messages.error(request, 'You need to log in first.')
        return redirect('tutors:tutor_login')

    try:
        tutor = Tutor.objects.get(username=username)
    except Tutor.DoesNotExist:
        messages.error(request, 'Tutor not found.')
        return redirect('tutors:tutor_login')

    query = request.GET.get('query', '').strip()

    # Search tutors and students
    tutors = Tutor.objects.filter(first_name__icontains=query) | Tutor.objects.filter(last_name__icontains=query)
    students = Student.objects.filter(fullname__icontains=query) | Student.objects.filter(course__icontains=query)

    # Get friend requests with related objects
    friend_requests = FriendRequest.objects.filter(receiver_tutor=tutor, status='pending').select_related(
        'sender_student', 'sender_tutor'
    )

    context = {
        'friend_requests': friend_requests,
        'tutors': tutors,
        'students': students,
        'query': query,
    }

    return render(request, 'tutors_dashboard.html', context)


    
