from django.db import models
from datetime import datetime

class Adresse(models.Model):
    id = models.IntegerField(primary_key=True)
    Ligne1 = models.CharField(max_length=255)
    ligne2 = models.CharField(max_length=255)
    code_postal = models.IntegerField()
    ville = models.CharField(max_length=255)

    def __str__(self):
       return f"Adresse: {self.Ligne1} {self.Ligne1}: ville {self.ville} code postal {self.code_postal}"

class Client(models.Model):
    id = models.IntegerField(primary_key=True)
    prenom = models.CharField(max_length=255)
    nom = models.CharField(max_length=255)
    adresse  = models.ForeignKey(Adresse, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
       return f"Prenom: {self.prenom} Nom: {self.nom}"

class Commande(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre_produits = models.IntegerField()
    montant = models.BigIntegerField()
    date_commande = models.DateField(default=datetime.now())
    client_id  = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
       return f"Nb produits: {self.nombre_produits} montant {self.montant} date commande {self.date_commande}"