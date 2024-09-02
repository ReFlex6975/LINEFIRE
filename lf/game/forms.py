from django import forms
from .models import GameFile


class GameFileForm(forms.ModelForm):
    class Meta:
        model = GameFile
        fields = ['file']


class EditGamerForm(forms.Form):
    gamer_id = forms.IntegerField(help_text='Enter the Gamer ID')
    new_name = forms.CharField(max_length=100, help_text='Enter the new name for the player')
