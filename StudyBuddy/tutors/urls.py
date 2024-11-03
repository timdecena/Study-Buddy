from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TutorViewSet  # Import your TutorViewSet
from django.views.generic import TemplateView  # Import TemplateView

# Create a router and register the TutorViewSet
router = DefaultRouter()
router.register(r'tutors', TutorViewSet)

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),  # Serve the main template at the root URL
    path('api/', include(router.urls)),  # Include API routes under /api/
]
