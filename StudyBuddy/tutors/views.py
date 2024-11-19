from rest_framework import viewsets
from .models import Tutor
from .serializers import TutorSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

class TutorViewSet(viewsets.ModelViewSet):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer

def tutor_login(request):
    """
    Displays the login form and handles the login process.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            # Find the tutor by username
            tutor = Tutor.objects.get(username=username)
            
            # Check if the password is correct (no hashing, directly comparing)
            if tutor.password == password:
                # If password is correct, manually log the tutor in
                request.session['tutor_id'] = tutor.id  # Store tutor's ID in session
                return redirect('/')  # Redirect to the home page or dashboard
            else:
                messages.error(request, 'Invalid username or password.')
        except Tutor.DoesNotExist:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')
        

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages  # For displaying feedback messages

def tutor_logout(request):
    """
    Logs out the tutor and redirects to the home page.
    """
    # Perform the logout
    logout(request)
    
    # Optionally add a success message for feedback
    messages.success(request, "You have been logged out successfully.")
    
    # Redirect to the home page or login page
    return redirect('/')
