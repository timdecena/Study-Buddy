from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Corrected 'admins/' to 'admin/'
    path('', include('home.urls')),  # Include home app's URLs at the root
    path('Course/', include('Course.urls')),
    path('students/', include('students.urls')),
    path('Subject/', include('Subject.urls')),
    path('tutors/', include('tutors.urls', namespace='tutors')),  # Correct namespace usage for tutors
    path('transaction/', include('transaction.urls')),
    path('session/', include('session.urls')),
    path('friend_requests/', include('friend_requests.urls', namespace='friend_requests')),  # Correct namespace for friend_requests
    path('another-students-path/', include('students.urls', namespace='students_alt')),  # Alternative namespace
    path('', include('home.urls')),  # Include home app URLs
    


]+ static(settings.STATIC_URL,document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
