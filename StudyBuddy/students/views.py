from django.shortcuts import render, redirect, get_object_or_404

from friend_requests.models import FriendRequest
from .models import Student
from .forms import StudentForm
from tutors.models import Tutor
from django.contrib import messages
from django.views.generic import UpdateView


# Student Login
def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate against the Student model
        try:
            student = Student.objects.get(username=username, password=password)
            
            # Set session data
            request.session['username'] = student.username
            request.session['user_role'] = 'student'
            
            messages.success(request, f"Login Successful")
            return redirect('students:student_homepage')  # Redirect to the student homepage
        except Student.DoesNotExist:
            messages.error(request, "Invalid username or password")
            return redirect('students:login')

    return render(request, 'students/student_login.html')

def student_homepage(request):
    # Check if the user is logged in and has the 'student' role
    if request.session.get('user_role') == 'student' and request.session.get('username'):
        try:
            # Retrieve the student object based on the username in the session
            student = get_object_or_404(Student, username=request.session['username'])
            return render(request, 'students/student_homepage.html', {'student': student})
        except Student.DoesNotExist:
            # Handle the case where the username does not match any student record
            messages.error(request, "Student profile not found.")
            return redirect('students:login')
    else:
        # If the user is not authorized, display an error message and redirect to the login page
        messages.error(request, "You are not authorized to access this page.")
        return redirect('students:login')

# List all students
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})

# Create a new student
def student_create(request,pk=None):
    if pk:
        student = get_object_or_404(Student, pk=pk)
    else:
        student = None
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            # Check if the user wants to delete the profile picture
            if form.cleaned_data.get('delete_profile_image'):
                student.profile_image = 'profile_pics/default.jpg'
            student.save()
            return redirect('students:student_list')  # Redirect to student list or another page
    else:
        form = StudentForm(instance=student)

    return render(request, 'students/student_form.html', {'form': form})

# Update an existing student
def student_update(request, pk):
    student = get_object_or_404(Student, student_id=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('students:student_list')  # Redirect to the student list or desired page
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_update.html', {'form': form, 'student': student})

# Delete a student
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, "Student deleted successfully!")
        return redirect('students:student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})

def logout(request):
    # Clear the session
    request.session.flush()
    # Optional: Add a logout success message
    messages.success(request, "You have been logged out successfully.")
    # Redirect to the default homepage
    return redirect('home')  # Change 'default_homepage' to the name of your homepage view

def tutors_list(request):
    # Assuming you have a Tutor model to query
    tutors = Tutor.objects.all()
    return render(request, 'students/tutors_list.html', {'tutors': tutors})

# students/views.py

def student_list(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    if query:
        students = Student.objects.filter(fullname__icontains=query)  # Filter students based on fullname
    else:
        students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students, 'query': query})

def view_students(request):
    students = Student.objects.all()  # Fetch all students
    return render(request, 'students/students_view.html', {'students': students})


def edit_profile(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('students:student_homepage')
    else:
        form = StudentForm(instance=student)

    return render(request, 'students/edit_profile.html', {'form': form, 'student': student})

def available_tutors(request):
    tutors = Tutor.objects.all()  # Available tutors
    accepted_tutors = Tutor.objects.filter(friend_requests__sender=request.user, friend_requests__status='accepted')
    
    return render(request, 'available_tutors.html', {
        'tutors': tutors,
        'accepted_tutors': accepted_tutors
    })

def handle_friend_request(request, request_id, action):
    friend_request = get_object_or_404(FriendRequest, pk=request_id)

    if action == 'accept':
        friend_request.status = 'accepted'
        if friend_request.sender_student:
            friend_request.receiver_tutor.accepted_students.add(friend_request.sender_student)
        elif friend_request.sender_tutor:
            friend_request.receiver_student.accepted_tutors.add(friend_request.sender_tutor)

        messages.success(request, 'Friend request accepted!')
    elif action == 'decline':
        friend_request.status = 'declined'
        messages.info(request, 'Friend request declined.')

    friend_request.save()
    return redirect('tutors:tutors_dashboard' if request.session.get('user_role') == 'tutor' else 'students:student_homepage')
   



