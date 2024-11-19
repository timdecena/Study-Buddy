from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TutorViewSet, tutor_login, tutor_logout  # Import required views
from django.views.generic import TemplateView

# Create a router and register the TutorViewSet
router = DefaultRouter()
router.register(r'tutors', TutorViewSet)

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('api/', include(router.urls)),
    path('course/', include('Course.urls')),
    path('login/', tutor_login, name='tutor_login'),
    path('logout/', tutor_logout, name='tutor_logout'),
]
