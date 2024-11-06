from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')  # Renders home.html from home/templates
