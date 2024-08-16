from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm
from .models import Buyer, Polygon


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    captcha = CaptchaField()


class RegisterForm(UserCreationForm):
    fio = forms.CharField(max_length=100, required=True)
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )

    class Meta(UserCreationForm):
        model = Buyer
        fields = ['username', 'password1', 'password2', 'fio', 'dob']

class PolygonForm(forms.ModelForm):
    class Meta:
        model = Polygon
        fields = ['title', 'description', 'image1', 'image2', 'image3', 'image4']

# ______________________________________________________________________________________


from django import forms
from .models import Scenario

class ScenarioForm(forms.ModelForm):
    class Meta:
        model = Scenario
        fields = ['title', 'description', 'video_url']