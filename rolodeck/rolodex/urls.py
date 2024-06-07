# urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import RolodexHomeView, add_person, custom_logout
from .views import UserLoginAPIView, UserCreateAPIView, PeopleAPIView, UserRegistrationAPIView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    path('', RolodexHomeView.as_view(), name='rolodex_home'),
    path('add/', add_person, name='add_person'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('api/login/', UserLoginAPIView.as_view(), name='user-login'),
    path('api/register/', UserCreateAPIView.as_view(), name='user-register'),
    path('api/people/', PeopleAPIView.as_view(), name='people_api'),
    path('api/signup/', UserRegistrationAPIView.as_view(), name='user-signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)