from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admins/', admin.site.urls),
    path('', include('home.urls')),  # Include home app's URLs at the root
    path('Course/', include('Course.urls')),
    path('students/', include('students.urls')),
    path('Subject/', include('Subject.urls')),
    path('tutors/', include('tutors.urls', namespace='tutors')),  # Include tutors URLs only once
    path('transaction/', include('transaction.urls')),
    path('session/', include('session.urls')),
    
]
