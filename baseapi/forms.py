from django.forms import ModelForm,TextInput
from .models import Movie



class MovieForm(ModelForm):
    class Meta:
        model=Movie
        fields=['title','overview','release','poster']
        
        