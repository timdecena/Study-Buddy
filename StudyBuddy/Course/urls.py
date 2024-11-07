# Course/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_management, name='course-management'),
    path('add/', views.add_course, name='add-course'),
    path('update/<int:course_id>/', views.update_course, name='update-course'),
    path('delete/<int:course_id>/', views.delete_course, name='delete-course')

]
