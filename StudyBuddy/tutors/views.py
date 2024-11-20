from rest_framework import viewsets
from .models import Tutor
from .serializers import TutorSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render

class TutorViewSet(viewsets.ModelViewSet):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer

def tutor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            tutor = Tutor.objects.get(username=username)
            if tutor.password == password:
                # Store tutor's details in session
                request.session['user_role'] = 'Tutor'
                request.session['username'] = tutor.username
                return redirect('/')
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
    
    messages.success(request, 'You have successfully logged out.')
    return redirect('/')

def ok(request):
    return render(request, 'login.html')
