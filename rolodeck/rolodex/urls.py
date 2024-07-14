# urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import RolodexHomeView, add_person, custom_logout
from .views import UserLoginAPIView, UserCreateAPIView, PeopleAPIView, UserRegistrationAPIView,ImportProfileAPIView, api_add_person,get_csrf_token,add_person_api,share_rolodeck,person_update,UserProfileAPIView,import_profile_by_code,ViewProfileCodeAPIView,UserProfileCreateAPIView,api_user_profile,import_profile_by_code,UserProfileView,create_or_update_user_profile,UserSelfProfileView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from rest_framework import routers
from .views import UploadViewSet
router = routers.DefaultRouter()
router.register(r'upload', UploadViewSet, basename="upload")
urlpatterns = [
    path('', RolodexHomeView.as_view(), name='rolodex_home'),
    path('add/', add_person, name='add_person'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('api/login/', UserLoginAPIView.as_view(), name='user-login'),
    path('api/register/', UserCreateAPIView.as_view(), name='user-register'),
    path('api/people/', PeopleAPIView.as_view(), name='people_api'),
    path('api/signup/', UserRegistrationAPIView.as_view(), name='user-signup'),
    path('api/add_person/', api_add_person, name='add_person'),
    path('api/get_csrf_token/', get_csrf_token, name='get_csrf_token'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/share_rolodeck/', share_rolodeck, name='share_rolodeck'),
    path('api/person-update/', person_update, name='person_update'),
    path('api/profile/<str:username>/', views.api_user_profile, name='api_user_profile'),
    path('api/user-profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('api/create-user-profile/', UserProfileCreateAPIView.as_view(), name='create_user_profile'),
    path('api/view-profile-code/', ViewProfileCodeAPIView.as_view(), name='view-profile-code'),
    path('api/user-profile-create/', create_or_update_user_profile, name='create_or_update_user_profile'),
    path('api/import-profile-by-code/', import_profile_by_code, name='import_profile_by_code'),
    path('api/userself-profile/', UserSelfProfileView.as_view(), name='userself-profile'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('', include(router.urls)),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)