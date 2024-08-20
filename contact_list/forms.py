from django import forms
from .models import Contact, Tag, Group
from registration.models import Usuario

class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact
        fields = ['first_name', 'last_name', 'phone', 'email', 'address', 'birthdate', 'group',]
        widgets = {
            'owner': forms.HiddenInput(),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('Usuario')
        super().__init__(*args, **kwargs)
        self.fields['owner'].initial = user
        self.fields['tags'].widget = forms.CheckboxSelectMultiple()