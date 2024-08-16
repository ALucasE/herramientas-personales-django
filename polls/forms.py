from django import forms
from django.forms.models import inlineformset_factory
from .models import Poll, Choice

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields=['title','question_text',]

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields=['choice_text',]
