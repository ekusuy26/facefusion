from django.shortcuts import render, loader, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,CreateView,DeleteView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from . import forms
from .forms import DogForm
from django.http import HttpResponse
from .models import Dog

class MyLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = "accounts/login.html"

class MyLogoutView(LoginRequiredMixin, LogoutView):
    template_name = "accounts/logout.html"

class IndexView(TemplateView):
    template_name = "index.html"

class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "accounts/create.html"
    success_url = reverse_lazy("login")

def regist(request):
    if request.method == 'GET':
        form = DogForm()
    else:
        form = DogForm(request.POST, request.FILES)
        form.instance.user_id = request.user.id
        if form.is_valid():
            print('dog_regist is_valid')
            form.save(request.POST)
            return redirect('show')
        else:
            print('dog_regist false is_valid')

    template = loader.get_template('accounts/dog.html')
    context = {
        'form': form,
    }
    return HttpResponse(template.render(context, request))

def show(request):
    dogs = Dog.objects.filter(user_id = request.user.id)
    return render(request, 'accounts/show.html', {'dogs': dogs})

class DogDelete(DeleteView):
    template_name = 'accounts/dog_delete.html'
    model = Dog
    success_url = reverse_lazy('show')

class DogUpdate(UpdateView):
    template_name = 'accounts/dog.html'
    model = Dog
    fields = ['image', 'dogname', 'age', 'sex', 'introduction']
    success_url = reverse_lazy('show')