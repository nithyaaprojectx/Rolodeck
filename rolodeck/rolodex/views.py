# views.py
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .models import Person
from .forms import PersonForm
from django.contrib.auth import logout
from django.shortcuts import redirect
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
