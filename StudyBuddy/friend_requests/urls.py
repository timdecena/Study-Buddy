# friend_requests/urls.py

from django.urls import path
from . import views

app_name = 'friend_requests'  # Ensure app name is included for URL resolution

urlpatterns = [
    
    path('send_friend_request/<int:tutor_id>/', views.send_friend_request, name='send_friend_request'),
    path('view_friend_requests/', views.view_friend_requests, name='view_friend_requests'),
    path('handle_friend_request/<int:request_id>/<str:action>/', views.handle_friend_request, name='handle_friend_request'),
]
