from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TutorViewSet, tutor_login, tutor_logout, tutor_list
from django.views.generic import TemplateView

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
    path('dashboard/', TemplateView.as_view(template_name='tutors_dashboard.html'), name='tutors_dashboard'),

    # Tutor management
    path('tutors_list/', tutor_list, name='tutor_list'),
]
