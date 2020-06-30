import os
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib import messages
#REST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

#Django Rest Framework
from rest_framework import viewsets
from .serializers import ClientSerializer

from .models import Adresse, Client, Commande
from .forms import ClientForm


# loas the messages for templatessss
with open(os.path.join(settings.BASE_DIR, "clients/static/messages.json"), encoding='utf-8') as f:
    msg = json.load(f)

# Create your views here.

def welcome(request):
    #return HttpResponse("Welcome to Django! ")
    #messages.add_message(request, messages.INFO, 'Hello world.')
    messages.info(request, 'Hello world..')
    return render(request, "clients/test.html")

def index(request):
    return render(request, "clients/client_liste.html",
            {"clients": Client.objects.all(),
             "msg": msg,
            })

def show(request, id):
    client = get_object_or_404(Client, pk=id)
    return render(request, "clients/client_consult.html", 
                 {"client": client,
                 "msg": msg,
                 })

def create(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"{msg['liste']['actions']['creerSucces']}  {form.instance.nom} {form.instance.prenom} ", 'success')
            return redirect("index")
    else:
        form = ClientForm()
    return render(request, "clients/client_fiche.html", 
                 {"form": form,
                 "clientId": -1,
                 "msg": msg,
                 })

def edit(request, id):
    client = get_object_or_404(Client, pk=id)
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, f"{msg['liste']['actions']['modifierSucces']} {form.instance.nom} {form.instance.prenom}")
            return redirect("index")
    else:
        form = ClientForm(instance=client)
    return render(request, "clients/client_fiche.html", 
                 {"form": form,
                 "clientId": id,
                 "msg": msg,
                 })

def delete(request,id):
    client = get_object_or_404(Client, pk=id)
    client.delete()
    messages.warning(request, f"{msg['liste']['actions']['supprimerSucces']}")
    return redirect("index")

# REST APi
def api_index(request):
    #clients = Client.objects.all().values('nom', 'prenom')  # or simply .values() to get all fields
    clients = Client.objects.all().values();
    clients_list = list(clients)  # important: convert the QuerySet to a list object
    return JsonResponse(clients_list, safe=False)

def api_show(request,id):
    try:
        client = Client.objects.get(pk=id)
        response = dict(
            id=client.id,
            prenom=client.prenom,
            nom=client.nom,
            adresse_id=client.adresse_id
        )
        return JsonResponse(response, safe=False)
    except Client.DoesNotExist:
        return JsonResponse({"error": 'Not found'})

@csrf_exempt
def api_create(request):
    if request.method == "POST":
         # process json data from request
        data = request.body.decode("utf-8")
        data = json.loads(data)
        nom    = None
        prenom = None
        error  = None

        if 'nom' in data:
            nom    = data['nom']    
        else:
            error = 'Nom requis.'

        if 'prenom' in data:
            prenom = data['prenom']
        else:
            error = 'Prenom requis.'

        if not error:
            #new client
            client = Client(nom=nom, prenom=prenom)
            client.save()
            
            print(f"{messages['liste']['actions']['creerSucces']}  {nom} {prenom} ", 'success')
            return api_index(request)
        
        print(error)
        return JsonResponse({"error": error})
    else:
         #GET
        return JsonResponse({"id":-1,"nom":"","prenom":"", "adresse_id": ""})

@csrf_exempt
def api_edit(request, id):
    try:
        if request.method == "POST":
            # process json data from request
            data = request.body.decode("utf-8")
            data = json.loads(data)
            id = None
            nom = None
            prenom = None
            error  = None

            #data_key = list(data.keys()) 
            #for key in data_key:
            #    print(data[key])

            if 'id' in data:
                id    = data['id']     
            else:
                error = 'Id requis in JSON request.'

            if 'nom' in data:
                nom    = data['nom']     
            else:
                error = 'Nom requis in JSON request.'

            if 'prenom' in data:
                prenom = data['prenom']
            else:
                error = 'Prenom requis in JSON request.'
        
            if not error:    
                #modified client  
                client = Client.objects.get(pk=id)
                client.nom = nom
                client.prenom = prenom
                client.save()
                print(f"{messages['liste']['actions']['modifierSucces']}  {nom} {prenom} ", 'success')
                return api_index(request)

            print(error)
            return JsonResponse({"error": error})
        else:
            #GET
            client = Client.objects.get(pk=id)              
            response = dict(
                id=client.id,
                prenom=client.prenom,
                nom=client.nom,
                adresse_id=client.adresse_id
            )
            return JsonResponse(response)
    except Client.DoesNotExist:
        return JsonResponse({"error": 'Not found'})

@csrf_exempt
def api_delete(request, id):
    try:
        if request.method in ["GET","DELETE"]:
            client = Client.objects.get(pk=id)  
            client.delete()
            print(f"{messages['liste']['actions']['supprimerSucces']}", 'warning')
        return api_index(request)
    except Client.DoesNotExist:
        return JsonResponse({"error": 'Not found'})

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()  #.order_by('nom')
    serializer_class = ClientSerializer
