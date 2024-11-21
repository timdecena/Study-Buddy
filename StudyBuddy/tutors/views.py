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
from tutors.models import Tutor
from students.models import Student

def tutors_dashboard(request):
    query = request.GET.get('query', '').strip()
    tutors = Tutor.objects.filter(first_name__icontains=query) | Tutor.objects.filter(last_name__icontains=query)
    students = Student.objects.filter(fullname__icontains=query) | Student.objects.filter(course__icontains=query)
    return render(request, 'tutors_dashboard.html', {
        'tutors': tutors,
        'students': students,
    })


from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Assignment

def assignment_page(request):
    if request.method == 'POST':
        # Print the form data to check if title and description are sent correctly
        title = request.POST.get('title')
        description = request.POST.get('description')
        assignment_id = request.POST.get('assignment_id')

        print(f"Title: {title}, Description: {description}")

        if not title or not description:
            return JsonResponse({'success': False, 'error': 'Title and description are required'}, status=400)

        if assignment_id:
            # Update existing assignment
            try:
                assignment = Assignment.objects.get(id=assignment_id)
                assignment.title = title
                assignment.description = description
                assignment.save()
            except Assignment.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Assignment not found'}, status=404)
        else:
            # Create new assignment
            Assignment.objects.create(title=title, description=description)

        return JsonResponse({'success': True})

    # Handle GET requests and show all assignments
    assignments = Assignment.objects.all()
    return render(request, 'assignment.html', {'assignments': assignments})

