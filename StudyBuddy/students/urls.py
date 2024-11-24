from django.urls import path
from . import views
from .views import tutors_list 

app_name = 'students'

urlpatterns = [
    path('login/', views.student_login, name='login'),
    path('homepage/', views.student_homepage, name='student_homepage'),
    path('', views.student_list, name='student_list'),
    path('create/', views.student_create, name='student_create'),
    path('update/<int:pk>/', views.student_update, name='student_update'),
    path('delete/<int:pk>/', views.student_delete, name='student_delete'),
    path('logout/', views.logout, name='logout'),
    path('view_tutors/', tutors_list, name='tutors_list'),  
    path('view/', views.view_students, name='view_students'),  # New URL
    

]
