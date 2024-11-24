from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TutorViewSet, tutor_login, tutor_logout, tutor_list, tutors_dashboard, assignment_page
from django.views.generic import TemplateView
from . import views
from .views import handle_friend_request

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

    #Assignment
    # Assignment Management
    path('assignments/', assignment_page, name='assignment'),
    
    path('handle_friend_request/<int:id>/<str:action>/', handle_friend_request, name='handle_friend_request'),



]
