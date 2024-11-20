from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from tutors.models import Tutor
from django.contrib import messages


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
            
            messages.success(request, f"Welcome, {student.fullname}!(Logged in as student)")
            return redirect('students:student_homepage')  # Redirect to the student homepage
        except Student.DoesNotExist:
            messages.error(request, "Invalid username or password")
            return redirect('students:login')

    return render(request, 'students/student_login.html')

# Student Homepage
def student_homepage(request):
    if request.session.get('user_role') == 'student':
        student = Student.objects.get(username=request.session['username'])
        return render(request, 'students/student_homepage.html', {'student': student})
    else:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('students:login')

# List all students
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})

# Create a new student
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student registered successfully!")
            return redirect('students:student_list')  # Redirect after success
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form})

# Update an existing student
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully!")
            return redirect('students:student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form})

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



