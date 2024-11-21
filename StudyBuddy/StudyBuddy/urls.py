from django.contrib import admin
from django.urls import path, include
from friend_requests.views import send_friend_request, handle_friend_request  # Import views from friend_requests

urlpatterns = [
    path('admins/', admin.site.urls),
    path('', include('home.urls')),  # Include home app's URLs at the root
    path('Course/', include('Course.urls')),
    path('students/', include('students.urls')),
    path('Subject/', include('Subject.urls')),
    path('tutors/', include('tutors.urls', namespace='tutors')),  # Include tutors URLs only once
    path('transaction/', include('transaction.urls')),
    path('session/', include('session.urls')),
    path('friend-requests/', include('friend_requests.urls')),
    

    # Specific route for sending friend request (before the general friend_requests include)
    path('friend_requests/send_friend_request/<int:tutor_id>/', send_friend_request, name='send_friend_request'),
    
    # The general include for friend requests
    path('friend_requests/', include('friend_requests.urls')),

    # Handling friend request actions
    path('handle_request/<int:request_id>/<str:action>/', handle_friend_request, name='handle_friend_request'),
]
