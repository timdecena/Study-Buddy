from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib import messages




def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate against Student model
        try:
            student = Student.objects.get(username=username, password=password)
            messages.success(request, f"Welcome, {student.fullname}!")
            return redirect('students:student_list')  # Redirect to the student list or profile
        except Student.DoesNotExist:
            messages.error(request, "Invalid username or password")
            return redirect('students:login')

    return render(request, 'students/student_login.html')

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
            return redirect('students:student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form})

# Delete a student
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('students:student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})