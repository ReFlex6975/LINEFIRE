from django import forms
from captcha.fields import CaptchaField

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Имя')
    email = forms.EmailField(label='Email')
    message = forms.CharField(widget=forms.Textarea, label='Сообщение')
    captcha = CaptchaField(label='Капча')