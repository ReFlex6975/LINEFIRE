from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm
from .models import Polygon, Scenario, CustomUser, Section, Equipment


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    captcha = CaptchaField()


class PolygonForm(forms.ModelForm):
    class Meta:
        model = Polygon
        fields = ['title', 'description', 'image1', 'image2', 'image3', 'image4']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control fs-5',
                'placeholder': 'Введите название полигона',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control fs-5',
                'rows': 4.,
                'placeholder': 'Введите описание полигона',
            }),
            'image1': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'image2': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'image3': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'image4': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'title': '',
            'description': '',
            'image1': '',
            'image2': '',
            'image3': '',
            'image4': '',
        }

# ______________________________________________________________________________________


class ScenarioForm(forms.ModelForm):
    class Meta:
        model = Scenario
        fields = ['title', 'description', 'video_url']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control fs-5',
                'style': 'background-color: white;',
                'placeholder': 'Введите название сценария',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control fs-5',
                'style': 'background-color: white;',
                'rows': 10,
                'placeholder': 'Опишите сценарий здесь',
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'form-control fs-5',
                'style': 'background-color: white;',
                'placeholder': 'Введите ссылку на видео',
            }),
        }
        labels = {
            'title': '',
            'description': '',
            'video_url': '',
        }


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
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control fs-5',
                'placeholder': 'Введите название оборудования',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control fs-5',
                'rows': 4,
                'placeholder': 'Введите описание оборудования',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control fs-5',
                'placeholder': 'Введите цену оборудования',
            }),
            'image1': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'image2': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'image3': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'image4': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'image5': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'name': '',
            'description': '',
            'price': '',
            'image1': '',
            'image2': '',
            'image3': '',
            'image4': '',
            'image5': '',
        }
