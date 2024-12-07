from django.shortcuts import render, redirect, get_object_or_404

from friend_requests.models import FriendRequest
from .models import Student
from .forms import StudentForm
from tutors.models import Tutor
from django.contrib import messages
from transaction.models import Transaction
from transaction.forms import TransactionForm
from tutors.models import Tutor



from django.shortcuts import render, redirect
from django.contrib import messages
from students.models import Student

def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            student = Student.objects.get(username=username)
            if student.password == password:  # Use secure password checking here
                request.session['username'] = student.username
                request.session['user_role'] = 'student'
                messages.success(request, "Login Successful")
                return redirect('students:student_homepage')  # Corrected URL name
            else:
                messages.error(request, "Invalid username or password")
                return redirect('students:student_login')  # Corrected URL name
        except Student.DoesNotExist:
            messages.error(request, "Invalid username or password")
            return redirect('students:student_login')  # Corrected URL name

    return render(request, 'students/student_login.html')


def student_homepage(request):
    # Check if the user is logged in and has the 'student' role
    if request.session.get('user_role') == 'student' and request.session.get('username'):
        try:
            # Retrieve the student object based on the username in the session
            student = get_object_or_404(Student, username=request.session['username'])
            
            # Fetch tutors who have accepted this student
            accepted_tutors = FriendRequest.objects.filter(
                sender_student=student, status='accepted'
            ).select_related('receiver_tutor')

            # Prepare the context data
            context = {
                'student': student,
                'accepted_tutors': [req.receiver_tutor for req in accepted_tutors],  # List of tutors who accepted
            }

            return render(request, 'students/student_homepage.html', context)
        
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
            return redirect('students:student_login')  # Redirect to student list or another page
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

def student_logout(request):  # Rename to match the URL pattern
    # Clear the session
    request.session.flush()
    # Optional: Add a logout success message
    messages.success(request, "You have been logged out successfully.")
    # Redirect to the default homepage
    return redirect('home')  # Update 'home' if needed

def tutors_list(request):
    # Fetch all tutors
    tutors = Tutor.objects.all()

    # Get the current logged-in user's role and username
    user_role = request.session.get('user_role')
    username = request.session.get('username')

    # Initialize friend_request_status
    friend_request_status = {}

    # Check if the user is a student or a tutor
    if user_role == 'student':
        # Fetch the logged-in student
        sender_student = Student.objects.get(username=username)

        # Get friend requests sent by the student
        friend_requests = FriendRequest.objects.filter(sender_student=sender_student)

        # Build a dictionary to map tutor IDs to request statuses
        friend_request_status = {
            req.receiver_tutor.id: req.status
            for req in friend_requests if req.receiver_tutor
        }
    elif user_role == 'tutor':
        # Fetch the logged-in tutor
        sender_tutor = Tutor.objects.get(username=username)

        # Get friend requests sent by the tutor (if applicable)
        friend_requests = FriendRequest.objects.filter(sender_tutor=sender_tutor)

        # Build a dictionary to map student IDs to request statuses (if needed)
        friend_request_status = {
            req.receiver_student.id: req.status
            for req in friend_requests if req.receiver_student
        }

    # Add the request status to each tutor
    for tutor in tutors:
        tutor.request_status = friend_request_status.get(tutor.id, None)

    # Pass the tutors and friend_request_status to the template
    return render(request, 'students/tutors_list.html', {
        'tutors': tutors,
    })

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
   

# views.py
def student_transactions(request):
    username = request.session.get('username')
    if not username:
        messages.error(request, 'You need to log in first.')
        return redirect('students:student_login')
    
    # Fetch transactions of the logged-in student
    transactions = Transaction.objects.filter(student__username=username)
    return render(request, 'students/transactions_list.html', {'transactions': transactions})


def create_transaction(request):
    username = request.session.get('username')
    if not username:
        messages.error(request, 'You need to log in first.')
        return redirect('students:student_login')
    
    # Get the logged-in student
    logged_in_student = get_object_or_404(Student, username=username)

    if request.method == 'POST':
        form = TransactionForm(request.POST, student=logged_in_student)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.student = logged_in_student
            transaction.save()
            messages.success(request, 'Transaction created successfully.')
            return redirect('students:create_transaction')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TransactionForm(student=logged_in_student)

    # Fetch all transactions for the logged-in student
    transactions = Transaction.objects.filter(student=logged_in_student).select_related('tutor')

    return render(request, 'students/create_transaction.html', {
        'form': form,
        'transactions': transactions,
    })
    

# students/views.py

def update_transaction_view(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('students:create_transaction')
        else:
            return render(request, 'students/update_transaction.html', {'form': form, 'error': 'Invalid data provided'})
    else:
        form = TransactionForm(instance=transaction)
        return render(request, 'students/update_transaction.html', {'form': form, 'transaction': transaction})

def delete_transaction_view(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    transaction.delete()
    return redirect('students:create_transaction')  # Or wherever you want to redirect

from django.shortcuts import render
from session.models import Session

def student_sessions(request):
    # Retrieve the username from the session
    username = request.session.get('username')
    if not username:
        messages.error(request, 'You need to log in first.')
        return redirect('students:student_login')

    # Get the logged-in student
    logged_in_student = get_object_or_404(Student, username=username)

    # Fetch all sessions for the logged-in student
    sessions = Session.objects.filter(student=logged_in_student).select_related('tutor', 'course')

    return render(request, 'students/session.html', {
        'sessions': sessions,
    })
    
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from tutors.models import Assignment
from students.models import Student

def assignment_list(request):
    # Retrieve the username from the session
    username = request.session.get('username')
    if not username:
        messages.error(request, 'You need to log in first.')
        return redirect('students:student_login')

    # Get the logged-in student
    logged_in_student = get_object_or_404(Student, username=username)

    # Fetch all assignments associated with this student
    assignments = Assignment.objects.filter(student=logged_in_student).select_related('tutor')

    return render(request, 'students/assignment.html', {
        'assignments': assignments,
    })

from .forms import AssignmentSubmissionForm


def submit_assignment(request):
    if request.method == "POST":
        assignment_id = request.POST.get('assignment_id')
        uploaded_file = request.FILES.get('file_upload')

        if not assignment_id or not uploaded_file:
            messages.error(request, "Please select an assignment and upload a file.")
            return redirect('students:student_homepage')

        try:
            assignment = get_object_or_404(Assignment, id=assignment_id)
            # Save the uploaded file
            assignment.file_upload = uploaded_file
            assignment.save()
            messages.success(request, "File uploaded successfully.")
        except Exception as e:
            messages.error(request, f"Error uploading file: {e}")

        return redirect('students:student_homepage')
    else:
        messages.error(request, "Invalid request.")
        return redirect('students:student_homepage')
