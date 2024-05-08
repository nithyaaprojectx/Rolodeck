# urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import RolodexHomeView, add_person, custom_logout

urlpatterns = [
    path('', RolodexHomeView.as_view(), name='rolodex_home'),
    path('add/', add_person, name='add_person'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', custom_logout, name='logout'),
]

