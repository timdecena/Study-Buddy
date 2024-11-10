from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('create/', views.student_create, name='student_create'),
    path('students/update/<slug:pk>/', views.student_update, name='student_update'),
    path('students/delete/<slug:pk>/', views.student_delete, name='student_delete'),  # Use pk as int
]
