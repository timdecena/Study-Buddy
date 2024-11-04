# students/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm

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
            return redirect('students:student_list')  # Updated with namespace
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
            return redirect('students:student_list')  # Updated with namespace
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form})

# Delete a student
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('students:student_list')  # Updated with namespace
    return render(request, 'students/student_confirm_delete.html', {'student': student})
