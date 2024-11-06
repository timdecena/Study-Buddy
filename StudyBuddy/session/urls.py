from django.urls import path
from . import views

urlpatterns = [
    path('', views.session_management, name='session-management'),
    path('add/', views.add_session, name='add-session'),
    path('update/<int:session_id>/', views.update_session, name='update-session'),
    path('delete/<int:session_id>/', views.delete_session, name='delete-session'),
]
