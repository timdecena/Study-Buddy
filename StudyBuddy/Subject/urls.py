# Subject/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.subject_management, name='subject-management'),
    path('add/', views.add_subject, name='add-subject'),
    path('update/<int:subject_id>/', views.update_subject, name='update-subject'),
    path('delete/<int:subject_id>/', views.delete_subject, name='delete-subject'),
]
