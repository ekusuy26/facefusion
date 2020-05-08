from django.shortcuts import render, loader, redirect
from django.http import HttpResponse
from .models import Chat
from accounts.models import Crew
from .forms import ChatForm
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    crews = Crew.objects.filter(users=request.user.id)
    return render(request, 'chat/index.html', {'crews' : crews})

def show(request, id):
    if request.method == 'GET':
        form = ChatForm()
    else:
        form = ChatForm(request.POST, request.FILES)
        form.instance.user_id = request.user.id
        form.instance.crew_id = id
        if form.is_valid():
            print('chat_regist is_valid')
            form.save(request.POST)
            return redirect('/chat/' + str(id))
        else:
            print('chat_regist false is_valid')

    crews = Crew.objects.filter(users=request.user.id)
    chats = Chat.objects.filter(crew_id=id)
    template = loader.get_template('chat/show.html')
    context = {
        'form': form,
        'chats' : chats,
        'crews' : crews,
    }
    return HttpResponse(template.render(context, request))