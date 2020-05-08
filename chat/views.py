from django.shortcuts import render, loader, redirect
from django.http import HttpResponse
from .models import Chat
from accounts.models import Crew
from .forms import ChatForm

# Create your views here.
def index(request):
    crews = Crew.objects.all()
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

    messages = Chat.objects.all()
    crews = Crew.objects.all()
    template = loader.get_template('chat/show.html')
    context = {
        'form': form,
        'messages' : messages,
        'crews' : crews,
    }
    return HttpResponse(template.render(context, request))