from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Polygon, Scenario, CustomUser, Section, Equipment
from django.contrib.auth.hashers import make_password


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    captcha = CaptchaField()


class PolygonForm(forms.ModelForm):
    class Meta:
        model = Polygon
        fields = ['title', 'description', 'image1', 'image2', 'image3', 'image4']


# ______________________________________________________________________________________


class ScenarioForm(forms.ModelForm):
    class Meta:
        model = Scenario
        fields = ['title', 'description', 'video_url']


# ______________________________________________________________________________________

class ManagerRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'manager'
        if commit:
            user.save()
        return user


class PlayerRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'player'
        if commit:
            user.save()
        return user

# ______________________________________________________________________________________


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['title', 'content']


# ______________________________________________________________________________________


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'description', 'price', 'image1', 'image2', 'image3', 'image4', 'image5']