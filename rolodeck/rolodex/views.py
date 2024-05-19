from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .models import Person
from .forms import PersonForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .serializers import UserSerializer, PersonSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get(self, request):
        username = request.query_params.get("username")
        password = request.query_params.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    def get_serializer_class(self):
        return UserSerializer

class PeopleAPIView(APIView):
    permission_classes = [AllowAny]  # Change to AllowAny to allow access without prior authentication

    def get(self, request):
        username = request.query_params.get("username")
        password = request.query_params.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Get people associated with the authenticated user
            people = Person.objects.filter(user=user)
            serializer = PersonSerializer(people, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.user = request.user
            person.save()
            return redirect('rolodex_home')
    else:
        form = PersonForm()
    return render(request, 'rolodex/add_person.html', {'form': form})
