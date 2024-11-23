from django.urls import path
from .views import home_view
from . import views

urlpatterns = [
    path('', home_view, name='home'),  # Home view will be rendered at the root path
    path('welcome/', views.welcome, name='welcome'),  # Welcome page
]
