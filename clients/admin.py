from django.contrib import admin
from .models import Adresse, Client, Commande

# Register your models here.
admin.site.register(Adresse)
admin.site.register(Client)
admin.site.register(Commande)