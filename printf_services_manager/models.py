from django.db import models

# Create your models here.
from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

class Projet(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Tache(models.Model):
    project = models.ForeignKey(Projet, on_delete=models.CASCADE)
    description = models.TextField()
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.description

class Facture(models.Model):
    project = models.ForeignKey(Projet, on_delete=models.CASCADE)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)
    due_date = models.DateField()

    def __str__(self):
        return "Facture pour le projet " + self.project.name
