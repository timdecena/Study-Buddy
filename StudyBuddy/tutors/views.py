from rest_framework import viewsets
from .forms import TutorRegistrationForm  # Make sure to create this form
from session.forms import SessionForm
from friend_requests.models import FriendRequest
from .models import Tutor
from .serializers import TutorSerializer
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json


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
    # Fetch the username from session data
    username = request.session.get('username')
    if not username:
        messages.error(request, 'You need to log in first.')
        return redirect('tutors:tutor_login')
    
    # Retrieve the logged-in tutor
    try:
        tutor = Tutor.objects.get(username=username)  # Get tutor by username from session
    except Tutor.DoesNotExist:
        messages.error(request, 'Tutor not found.')
        return redirect('tutors:tutor_login')

    # Handle search query for tutors and students
    query = request.GET.get('query', '').strip()
    
    # Search tutors by first name or last name
    tutors = Tutor.objects.filter(
        first_name__icontains=query
    ) | Tutor.objects.filter(
        last_name__icontains=query
    ) if query else Tutor.objects.none()
    
    # Search students by fullname or course
    students = Student.objects.filter(
        fullname__icontains=query
    ) | Student.objects.filter(
        course__icontains=query
    ) if query else Student.objects.none()
    
    # Fetch friend requests where the logged-in tutor is the receiver
    friend_requests = FriendRequest.objects.filter(
        receiver_tutor=tutor, status='pending'
    ).select_related('sender_student', 'sender_tutor', 'receiver_student', 'receiver_tutor')

    # Fetch accepted students for the logged-in tutor
    accepted_students = FriendRequest.objects.filter(
        receiver_tutor=tutor, status='accepted', sender_student__isnull=False
    ).select_related('sender_student')

    # Combine the context data
    context = {
        'friend_requests': friend_requests,  # Friend requests for the logged-in tutor
        'tutors': tutors,  # Tutors matching the search query
        'students': students,  # Students matching the search query
        'accepted_students': [req.sender_student for req in accepted_students],  # Accepted students
        'query': query,  # To retain the search query for displaying in the form
    }

    return render(request, 'tutors_dashboard.html', context)


from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Assignment
from tutors.models import Tutor

def assignment_page(request):
    if request.method == "POST":
        # Handle DELETE
        if request.headers.get('Content-Type') == 'application/json':
            try:
                body = json.loads(request.body)  # Parse JSON body
                assignment_id = body.get('delete_id')
                if assignment_id:
                    assignment = get_object_or_404(Assignment, id=assignment_id)
                    assignment.delete()
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'success': False, 'error': 'Invalid assignment ID'}, status=400)
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)

        # Handle Create/Update
        try:
            assignment_id = request.POST.get('assignment_id')
            title = request.POST.get('title')
            description = request.POST.get('description')
            student_id = request.POST.get('student_id')

            student = get_object_or_404(Student, student_id=student_id)

            if assignment_id:  # Update
                assignment = get_object_or_404(Assignment, id=assignment_id)
                assignment.title = title
                assignment.description = description
                assignment.student = student
            else:  # Create
                assignment = Assignment(title=title, description=description, student=student)

            assignment.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    # For GET requests or unexpected methods
    assignments = Assignment.objects.select_related('student').all()
    accepted_students = Student.objects.all()
    return render(request, 'assignment.html', {
        'assignments': assignments,
        'accepted_students': accepted_students,
    })

def assignment_view(request):
    tutor = get_object_or_404(Tutor, user=request.user)
    accepted_students = FriendRequest.objects.filter(
        receiver_tutor=tutor, status='accepted'
    ).values_list('sender_student', flat=True)
    students = Student.objects.filter(id__in=accepted_students)

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        title = request.POST.get('title')
        description = request.POST.get('description')

        if student_id and title and description:
            student = get_object_or_404(Student, id=student_id)
            Assignment.objects.create(
                tutor=tutor, student=student, title=title, description=description
            )
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Missing fields'})

    assignments = Assignment.objects.filter(tutor=tutor)
    return render(
        request, 'assignment.html',
        {'assignments': assignments, 'students': students}
    )



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

from django.shortcuts import get_object_or_404, redirect

def handle_friend_request(request, id, action):
    """
    Handles accepting or rejecting friend requests.
    """
    friend_request = get_object_or_404(FriendRequest, id=id)

    if action == 'accept':
        friend_request.status = 'accepted'
        messages.success(request, 'Friend request accepted.')
    elif action == 'reject':
        friend_request.status = 'rejected'
        messages.success(request, 'Friend request rejected.')
    else:
        messages.error(request, 'Invalid action.')

    friend_request.save()
    return redirect('tutors:tutors_dashboard')


def tutor_register(request):
    """
    Handles tutor registration functionality.
    """
    if request.method == 'POST':
        form = TutorRegistrationForm(request.POST)
        if form.is_valid():
            # Save the new tutor to the database
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('tutors:tutor_login')  # Redirect to the login page after registration
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TutorRegistrationForm()

    return render(request, 'register.html', {'form': form})

def create_session(request):
    username = request.session.get('username')
    if not username:
        messages.error(request, 'You need to log in first.')
        return redirect('tutors:tutor_login')
    
    try:
        logged_in_tutor = Tutor.objects.get(username=username)
    except Tutor.DoesNotExist:
        messages.error(request, 'Tutor not found.')
        return redirect('tutors:tutor_login')

    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.tutor = logged_in_tutor
            session.save()
            messages.success(request, 'Session created successfully.')
            return redirect('tutors:tutors_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SessionForm()
        accepted_students = FriendRequest.objects.filter(
            receiver_tutor=logged_in_tutor, status='accepted'
        ).values_list('sender_student__student_id', flat=True)  # Adjust for custom primary key
        form.fields['student'].queryset = Student.objects.filter(student_id__in=accepted_students)

    return render(request, 'create_session.html', {'form': form})



def tutor_profile(request):
    """
    Displays and updates the tutor profile.
    """
    if not request.session.get('username'):
        messages.error(request, "Please log in to access your profile.")
        return redirect('tutors:tutor_login')

    try:
        tutor = Tutor.objects.get(username=request.session['username'])
    except Tutor.DoesNotExist:
        messages.error(request, "Tutor not found.")
        return redirect('tutors:tutor_login')

    if request.method == 'POST':
        tutor.first_name = request.POST.get('first_name', tutor.first_name)
        tutor.last_name = request.POST.get('last_name', tutor.last_name)
        tutor.email = request.POST.get('email', tutor.email)
        tutor.username = request.POST.get('username', tutor.username)
        new_password = request.POST.get('password')

        if new_password:
            tutor.password = new_password  # Replace with proper password hashing in production
        tutor.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('tutors:tutor_profile')

    return render(request, 'tutor_profile.html', {'tutor': tutor})

    
@login_required
def remove_accepted_student(request, student_id):
    if request.method == 'POST':
        student = get_object_or_404(Student, student_id=student_id)
        tutor = Tutor.objects.get(user=request.user)  # Assuming a Tutor is linked to a user
        # Remove the student from the tutor's accepted list
        tutor.accepted_students.remove(student)
        return redirect('tutors:tutors_dashboard')  # Redirect to the tutor's dashboard
    return redirect('tutors:tutors_dashboard')

@csrf_exempt  # Make sure CSRF token is handled correctly in production
def delete_assignment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        assignment_id = data.get('delete_id')
        
        try:
            assignment = Assignment.objects.get(id=assignment_id)
            assignment.delete()
            return JsonResponse({'success': True})
        except Assignment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Assignment not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})