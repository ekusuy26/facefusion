from django.shortcuts import render, loader, redirect
from django.http import HttpResponse
from .models import Chat
from .forms import ChatForm

# Create your views here.
def index(request):
    if request.method == 'GET':
        form = ChatForm()
    else:
        form = ChatForm(request.POST, request.FILES)
        form.instance.user_id = request.user.id
        if form.is_valid():
            print('chat_regist is_valid')
            form.save(request.POST)
            return redirect('/chat')
        else:
            print('chat_regist false is_valid')

    messages = Chat.objects.all()
    template = loader.get_template('chat/index.html')
    context = {
        'form': form,
        'messages' : messages,
    }
    return HttpResponse(template.render(context, request))
