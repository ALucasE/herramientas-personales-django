from django import forms
from django.forms import ValidationError
import re
from django.core.validators import RegexValidator

#Validacion solo letras y espacios
def validate_letters_and_spaces(value):
    if not re.match(r'^[a-zA-Z\s]*$', value):
        raise ValidationError(
            'El campo solo puede contener letras',
            params={'value': value},
        )


class ContactForm(forms.Form):
    name = forms.CharField(
        label='Nombre y apellido',
        required=True,
        min_length=3,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Juan Perez'}),
    )
    phone = forms.CharField(
        label='Numero de telefono',
        validators=[RegexValidator(r'^(\+54)?\d{10}$', message='Ingrese un número válido - 11 1234 1234 / 351 123 1234')],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '54 11 1234 1234'})
        )
    email = forms.EmailField(
        label='Correo electronico',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'mail@mail.com'}),
    )
    confirm_email = forms.EmailField(
        label='Confirma el correo electronico',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'mail@mail.com'}),
    )
    subject = forms.CharField(
        label='Asunto',
        max_length=100,
        required=True,
        validators=[validate_letters_and_spaces],
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Motivo del contacto'})
    )
    message = forms.CharField(
        label='Mensaje',
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí su mensaje...', 'rows': 5}),
    )

    #CLEANS
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not all(x.isalpha() or x.isspace() for x in name):
            raise forms.ValidationError('El nombre no puede contener numero')
        return name

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        confirm_email = cleaned_data.get('confirm_email')

        if email != confirm_email:
            raise forms.ValidationError('Los correos electrónicos no coinciden.')
