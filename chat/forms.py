from django.contrib.auth import forms as auth_forms
from django import forms
from .models import Chat
from accounts.models import Crew

class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ('text',)

class CrewForm(forms.ModelForm):
    class Meta:
        model = Crew
        fields = ('name',)
