from rest_framework import viewsets
from .models import Tutor
from .serializers import TutorSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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


def tutor_list(request):
    """
    Renders a list of all tutors.
    """
    tutors = Tutor.objects.all()
    return render(request, 'tutors_list.html', {'tutors': tutors})
def ok(request):
    return render(request, 'login.html')

# tutors/views.py

def tutor_list(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    if query:
        tutors = Tutor.objects.filter(first_name__icontains=query)  # Filter tutors based on first name
    else:
        tutors = Tutor.objects.all()
    return render(request, 'tutors/tutor_list.html', {'tutors': tutors, 'query': query})


from django.shortcuts import render
from .models import Tutor
from students.models import Student  # Ensure you import Student model from the students app

def tutors_dashboard(request):
    query = request.GET.get('query', '')  # Get the search query from GET request

    # Initially, fetch all tutors and students
    tutors = Tutor.objects.all()
    students = Student.objects.all()

    if query:
        # Filter tutors based on first_name, last_name, or subject
        tutors = tutors.filter(
            first_name__icontains=query) | tutors.filter(last_name__icontains=query) | tutors.filter(subject__icontains=query)

        # Filter students based on fullname or course
        students = students.filter(
            fullname__icontains=query) | students.filter(course__icontains=query)

    context = {
        'tutors': tutors,
        'students': students,
        'query': query  # Passing query for feedback in the template
    }

    return render(request, 'tutors/dashboard.html', context)


