from django.urls import path
from . import views

app_name = 'friend_requests'

urlpatterns = [
    path('send/<str:receiver_type>/<int:receiver_id>/', views.send_friend_request, name='send_request'),
    path('handle/<int:request_id>/<str:action>/', views.handle_friend_request, name='handle_request'),
    path('list/', views.list_friend_requests, name='list_requests'),

]
