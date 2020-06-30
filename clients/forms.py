from datetime import date

from django.forms import ModelForm, DateInput, TimeInput, TextInput, IntegerField
from django.core.exceptions import ValidationError

from .models import Client


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'prenom']
        #use widgets with {{ form.nom|add_class:"form-control"|attr:"required" }} in template
        # widgets = {
        #     'nom': TextInput(attrs={"type": "text", 'placeholder':'nom obligatoire'}),
        #     'prenom': TextInput(attrs={"type": "text", 'placeholder':'prenom obligatoire'})
        # }