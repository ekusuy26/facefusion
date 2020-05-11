from django import forms
from .models import Document
 
 
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('photo', 'photo_two', 'out_put', 'out_put_two',)