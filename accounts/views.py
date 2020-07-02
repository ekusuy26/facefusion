from django.shortcuts import render, loader, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,CreateView,DeleteView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.urls import reverse_lazy, reverse
from . import forms
from .forms import DogForm
from django.http import HttpResponse
from .models import Dog, Like, Crew

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
            return redirect('myhp:toppage')
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

def dogShow(request, pk):
    dog = Dog.objects.get(id = pk)
    query = Like.objects.filter(user_id=request.user.id, dog_id=pk)
    if query.count() == 0:
        like_flg = 0
    else:
        like_flg = 1
    return render(request, 'accounts/dog_show.html', {
        'dog': dog,
        'like_flg': like_flg,
        })

class DogDelete(DeleteView):
    template_name = 'accounts/dog_delete.html'
    model = Dog
    success_url = reverse_lazy('myhp:toppage')

class DogUpdate(UpdateView):
    template_name = 'accounts/dog.html'
    model = Dog
    fields = ['image', 'dogname', 'age', 'sex', 'introduction']
    success_url = reverse_lazy('myhp:toppage')

def like(request, pk):
    query = Like.objects.filter(user_id=request.user.id, dog_id=pk)
    if query.count() == 0:
        # いいねする処理
        likes_tbl = Like()
        likes_tbl.user_id = request.user.id
        likes_tbl.dog_id = pk
        likes_tbl.save()
        dog = Dog.objects.get(id = pk)
        dog.like_num += 1
        dog.save()
        # 相手がログインユーザーをいいねしているか確認
        opponent_id = Dog.objects.get(id=pk).user.id
        check = Like.objects.filter(user_id=opponent_id, dog_id=request.user.dog.id)
        if check.count() == query.count():
            crews_tbl = Crew()
            crews_tbl.name = 'group' + str(request.user.id)
            crews_tbl.save()
            new_crew = Crew.objects.latest('id')
            new_crew.users.add(request.user)
            new_crew.users.add(opponent_id)
            return redirect('/chat/')
    else:
        # いいね外す処理
        query.delete()
        dog = Dog.objects.get(id = pk)
        dog.like_num -= 1
        dog.save()
    return redirect('/dog/' + str(pk))

# いいねした相手
def likedPerson(request):
    all_likes = Like.objects.filter(user_id=request.user.id)
    paginator = Paginator(all_likes, 5)
    p = request.GET.get('p')
    likes = paginator.get_page(p)
    headLine = 'じぶんからのいいね！'
    return render(request, 'myhp/liked_person.html', {
        'likes': likes,
        'headLine': headLine,
    })

# いいねされた相手
def likedOpponent(request):
    likes = Like.objects.filter(dog_id=request.user.dog.id)
    headLine = 'あいてからのいいね！'
    return render(request, 'myhp/liked_opponent.html', {
        'likes': likes,
        'headLine': headLine,
    })
