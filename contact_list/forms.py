from django import forms
from .models import Contact, Tag, Group
from registration.models import Usuario

class TagForm(forms.ModelForm):
    class Meta:
        model=Tag
        fields = ['name', 'color', 'contacts']



class GroupForm(forms.ModelForm):
    class Meta:
        model=Group
        fields = ['name',]
