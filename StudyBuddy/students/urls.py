from django.urls import path
from . import views
from .views import tutors_list

app_name = 'students'

urlpatterns = [
    path('login/', views.student_login, name='student_login'),  # Login URL
    path('homepage/', views.student_homepage, name='student_homepage'),  # Homepage URL
    path('', views.student_list, name='student_list'),  # Default student list
    path('create/', views.student_create, name='student_create'),  # Create student
    path('update/<int:pk>/', views.student_update, name='student_update'),  # Update student
    path('delete/<int:pk>/', views.student_delete, name='student_delete'),  # Delete student
    path('logout/', views.student_logout, name='student_logout'),  # Renamed logout
    path('view_tutors/', tutors_list, name='tutors_list'),  # Tutors list
    path('view/', views.view_students, name='view_students'),  # View students
    path('edit/<int:pk>/', views.edit_profile, name='edit_profile'),  # Edit profile
]
