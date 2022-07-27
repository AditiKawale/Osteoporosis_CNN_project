from django import forms
from .models import Imagemodel

class ImageForm(forms.ModelForm):
    class Meta:
        model=Imagemodel
        fields='__all__'
        labels={'photo':''}
        
