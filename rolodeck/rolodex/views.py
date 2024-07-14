from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .models import Person
from .forms import PersonForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, parser_classes, permission_classes
from django.contrib.auth.models import User
from .models import Person
from .serializers import PersonSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
import os
import threading
import time
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from .serializers import UserSerializer, PersonSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .serializers import UserRegistrationSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from .models import Person
from .serializers import PersonSerializer
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Person
from .serializers import PersonSerializer
from django.http import JsonResponse
from django.middleware.csrf import get_token
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import imghdr
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import UploadSerializer,PersonEditSerializer

def get_csrf_token(request):
    # Generate CSRF token
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token})

@api_view(['POST'])
@permission_classes([AllowAny])  # Adjust permissions as needed
def import_profile_by_code(request):
    code = request.data.get('code')  # Assuming 'code' is sent in the request data
    user_to_import = get_object_or_404(Person, codeu=code)

    serializer = PersonSerializer(data={
        'user': request.user.pk,  # Use the primary key of the authenticated user
        'name': user_to_import.name,
        'organization': user_to_import.organization,
        'hobby': user_to_import.hobby,
        'date_of_birth': user_to_import.date_of_birth,
        'phone_number': user_to_import.phone_number,
        'mail': user_to_import.mail,
        'interests': user_to_import.interests,
        'instagram': user_to_import.instagram,
        'twitter': user_to_import.twitter,
        'linkedin': user_to_import.linkedin,
        'youtube': user_to_import.youtube,
        'address': user_to_import.address,
        'projects': user_to_import.projects,
        'is_phone_verified': user_to_import.is_phone_verified,
        'otp': user_to_import.otp,
        'pronouns': user_to_import.pronouns,
        'notes': user_to_import.notes,
        'profilepic': user_to_import.profilepic,
    })

    if serializer.is_valid():
        serializer.save()  # Save the validated data to create a new Person instance
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_add_person(request):
    form = PersonForm(request.POST, request.FILES)
    if form.is_valid():
        person = form.save(commit=False)
        person.user = request.user
        person.save()
        serializer = PersonSerializer(person, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
class UserProfileCreateAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        name = request.data.get('name')
        organization = request.data.get('organization')
        hobby = request.data.get('hobby')
        date_of_birth = request.data.get('date_of_birth')
        phone_number = request.data.get('phone_number')
        mail = request.data.get('mail')
        interests = request.data.get('interests')
        instagram = request.data.get('instagram')
        twitter = request.data.get('twitter')
        linkedin = request.data.get('linkedin')
        youtube = request.data.get('youtube')
        address = request.data.get('address')
        projects = request.data.get('projects')
        is_phone_verified = request.data.get('is_phone_verified')
        otp = request.data.get('otp')
        pronouns = request.data.get('pronouns')
        notes = request.data.get('notes')
        profilepic = request.data.get('profilepic')

        # Create a new User instance
        user = User.objects.create_user(username=username, password=password)

        # Create a corresponding Person (UserProfile) instance
        new_person = Person.objects.create(
            user=user,
            name=name,
            organization=organization,
            hobby=hobby,
            date_of_birth=date_of_birth,
            phone_number=phone_number,
            mail=mail,
            interests=interests,
            instagram=instagram,
            twitter=twitter,
            linkedin=linkedin,
            youtube=youtube,
            address=address,
            projects=projects,
            pronouns=pronouns,
            code=generate_code(),  # Generate a new unique code for the profile
            notes=notes,
            profilepic=profilepic,
        )

        serializer = PersonSerializer(new_person)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    try:
        person = Person.objects.get(user=user, userself=True)
        serializer = PersonSerializer(person)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Person.DoesNotExist:
        return Response({"detail": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_user_profile(request, username):
    # Retrieve the person object associated with the username
    person = get_object_or_404(Person, user__username=username)

    if request.method == 'GET':
        serializer = PersonSerializer(person, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PersonSerializer(person, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Retrieve the current user's profile
        user = self.request.user
        return Person.objects.get(user=user)

    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Person.DoesNotExist:
            # If the profile doesn't exist, create it
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()
class UserProfileCreateAPIView(APIView):
    def post(self, request):
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return Response({"error": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)

        # Use the authenticated user's username as the profile name
        username = request.user.username

        # Extract other profile data from the request
        organization = request.data.get('organization')
        hobby = request.data.get('hobby')
        date_of_birth = request.data.get('date_of_birth')
        phone_number = request.data.get('phone_number')
        mail = request.data.get('mail')
        interests = request.data.get('interests')
        instagram = request.data.get('instagram')
        twitter = request.data.get('twitter')
        linkedin = request.data.get('linkedin')
        youtube = request.data.get('youtube')
        address = request.data.get('address')
        projects = request.data.get('projects')
        is_phone_verified = request.data.get('is_phone_verified')
        otp = request.data.get('otp')
        pronouns = request.data.get('pronouns')
        notes = request.data.get('notes')
        profilepic = request.data.get('profilepic')

        # Create or update the user profile
        person, created = Person.objects.update_or_create(
            user=request.user,  # Assuming Person model has a ForeignKey to User model
            defaults={
                'name': username,  # Use username as the profile name
                'organization': organization,
                'hobby': hobby,
                'date_of_birth': date_of_birth,
                'phone_number': phone_number,
                'mail': mail,
                'interests': interests,
                'instagram': instagram,
                'twitter': twitter,
                'linkedin': linkedin,
                'youtube': youtube,
                'address': address,
                'projects': projects,
                'is_phone_verified': is_phone_verified,
                'otp': otp,
                'pronouns': pronouns,
                'notes': notes,
                'profilepic': profilepic,
            }
        )

        # Return a response based on whether a new profile was created or updated
        if created:
            return Response({"message": "User profile created successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "User profile updated successfully."}, status=status.HTTP_200_OK)
class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        username = request.query_params.get("username")
        password = request.query_params.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        username = request.query_params.get('username')
        password = request.query_params.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            person = Person.objects.filter(user=user).first()
            if person:
                serializer = PersonSerializer(person, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class PeopleAPIView(APIView):
    permission_classes = [AllowAny]  # Allow access without prior authentication

    def get(self, request):
        username = request.query_params.get("username")
        password = request.query_params.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Get people associated with the authenticated user
            people = Person.objects.filter(user=user, userself=False)
            serializer = PersonSerializer(people, many=True, context={'request': request})  # Pass request context here
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
class ImportProfileAPIView(APIView):
    def post(self, request):
        code = request.data.get('code')
        user = request.user

        try:
            # Retrieve the person object based on the provided code
            person = get_object_or_404(Person, code=code)

            # Prevent importing the user's own profile
            if person.user == user:
                return Response({"error": "You cannot import your own profile"}, status=status.HTTP_400_BAD_REQUEST)

            # Create a new Person object with fields copied from the imported profile
            new_person = Person.objects.create(
                user=user,
                name=person.name,
                organization=person.organization,
                hobby=person.hobby,
                date_of_birth=person.date_of_birth,
                phone_number=person.phone_number,
                mail=person.mail,
                interests=person.interests,
                instagram=person.instagram,
                twitter=person.twitter,
                linkedin=person.linkedin,
                youtube=person.youtube,
                address=person.address,
                projects=person.projects,
                pronouns=person.pronouns,
                profilepic=person.profilepic,  # Assuming you want to copy the profile picture
            )



            return Response({"message": "Profile imported successfully"}, status=status.HTTP_201_CREATED)

        except Person.DoesNotExist:
            return Response({"error": "Profile not found with this code"}, status=status.HTTP_404_NOT_FOUND)
class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ViewProfileCodeAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        username = request.query_params.get('username')
        password = request.query_params.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                person = Person.objects.filter(user=user).first()
                if person:
                    return Response({"code": person.codeu}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
            except Person.DoesNotExist:
                return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class RolodexHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'rolodex/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['people'] = Person.objects.filter(user=self.request.user)
        return context

def custom_logout(request):
    logout(request)
    return redirect('login')

def add_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            person = form.save(commit=False)
            person.user = request.user
            person.save()
            return redirect('rolodex_home')
    else:
        form = PersonForm()
    return render(request, 'rolodex/add_person.html', {'form': form})

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([permissions.IsAuthenticated])
def add_person_api(request):
    serializer = PersonSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer

class UploadViewSet(ViewSet):
    serializer_class = UploadSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        file_uploaded = request.FILES.get('file_uploaded')
        content_type = file_uploaded.content_type
        response = "POST API and you have uploaded a {} file".format(content_type)
        return Response(response)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def person_update(request):
    username = request.data.get('username')
    password = request.data.get('password')
    person_name = request.data.get('name')

    # Authenticate user
    user = authenticate(username=username, password=password)
    if user is None:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        person = Person.objects.get(name=person_name, user=user)
    except Person.DoesNotExist:
        return Response({'error': 'Person not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = PersonEditSerializer(person, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def share_rolodeck(request):
    sharing_code = request.data.get('sharing_code')
    try:
        person = Person.objects.get(sharing_code=sharing_code)
    except Person.DoesNotExist:
        return Response({'error': 'Invalid sharing code.'}, status=status.HTTP_400_BAD_REQUEST)

    # Clone the person instance for the current user
    cloned_person = Person.objects.create(
        user=request.user,
        name=person.name,
        organization=person.organization,
        hobby=person.hobby,
        date_of_birth=person.date_of_birth,
        phone_number=person.phone_number,
        mail=person.mail,
        interests=person.interests,
        instagram=person.instagram,
        twitter=person.twitter,
        linkedin=person.linkedin,
        youtube=person.youtube,
        address=person.address,
        projects=person.projects,
        pronouns=person.pronouns,
        profilepic=person.profilepic,
    )


    serializer = PersonSerializer(cloned_person, context={'request': request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserSelfProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        username = request.GET.get('username')
        password = request.GET.get('password')

        # Perform authentication using username and password
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'detail': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Retrieve the user's own profile
            user_profile = Person.objects.get(user=user, userself=True)
            serializer = PersonSerializer(user_profile, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Person.DoesNotExist:
            return Response({'detail': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_or_update_user_profile(request):
    user = request.user
    data = request.data.copy()
    data['user'] = user.id
    data['userself'] = True  # Ensure the profile is marked as userself

    try:
        # Try to get the existing profile marked as userself
        person = Person.objects.get(user=user, userself=True)
        serializer = PersonSerializer(person, data=data)
    except Person.DoesNotExist:
        # If no existing profile, create a new one
        serializer = PersonSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)