from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')  # Renders home.html from home/templates

def welcome(request):
    return render(request, 'welcome.html')  # Render the welcome page


