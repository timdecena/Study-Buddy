from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TutorViewSet,
    tutor_login,
    tutor_logout,
    tutor_list,
    tutors_dashboard,
    assignment_page,
    tutor_profile,
    handle_friend_request,
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
    path('register/', views.tutor_register, name='tutor_register'),
    path('logout/', tutor_logout, name='tutor_logout'),

    # Dashboard
    path('dashboard/', tutors_dashboard, name='tutors_dashboard'),
    path('accept_friend_request/<int:id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:id>/', views.reject_friend_request, name='reject_friend_request'),

    # Tutor management
    path('tutors_list/', tutor_list, name='tutor_list'),
    path('create-session/', views.create_session, name='create_session'),
    path('view-sessions/', views.view_sessions, name='view_sessions'),  # New URL for View Sessions
    path('remove-accepted-student/<int:student_id>/', views.remove_accepted_student, name='remove_accepted_student'),


    # Assignment Management
    path('assignments/', assignment_page, name='assignment'),
    path('assignments/delete/', assignment_page, name='delete_assignment'),


    # Friend Request Handling
    path('handle_friend_request/<int:id>/<str:action>/', handle_friend_request, name='handle_friend_request'),
    path('remove-student/<int:student_id>/', views.remove_student, name='remove_student'),
    # Profile Management
    path('profile/', tutor_profile, name='tutor_profile'),  # Added profile path

    path('create-session/', views.create_session, name='create_session'),
    path('edit-session/<int:session_id>/', views.edit_session, name='edit_session'),  # Update session
    path('delete-session/<int:session_id>/', views.delete_session, name='delete_session'),  # Delete session
]
