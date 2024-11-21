from django import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TutorViewSet, 
    tutor_login, 
    tutor_logout,
    tutors_dashboard, 
    tutors_list, 
    send_friend_request, 
    handle_friend_request
)
from django.views.generic import TemplateView
from . import views

# Create a router and register the TutorViewSet
app_name = 'tutors'  # Define the namespace for reverse URL lookups
router = DefaultRouter()
router.register(r'tutors', TutorViewSet)

urlpatterns = [
    # API routes
    path('api/', include(router.urls)),

    # Public pages
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('login/', tutor_login, name='tutor_login'),
    path('logout/', tutor_logout, name='tutor_logout'),

    # Dashboard
    path('dashboard/', tutors_dashboard, name='tutors_dashboard'),
    path('accept_friend_request/<int:id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:id>/', views.reject_friend_request, name='reject_friend_request'),

    # Tutor management
    path('tutors_list/', tutors_list, name='tutors_list'),
    

    # Friend Requests
     path('send_friend_request/<int:tutor_id>/', send_friend_request, name='send_friend_request'),
    path('handle_friend_request/<int:request_id>/<str:action>/', handle_friend_request, name='handle_friend_request'),
]
