from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return 'Client {self.user}'

class Animal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    tag = models.AutoField(primary_key=True)
    breed = models.CharField(max_length=200, null=True)
    sex = models.CharField(max_length=200, null=True)
    weight = models.FloatField()
    years = models.CharField(max_length=200, null=True, blank=True)
    diseases = models.CharField(max_length=1000, null=True, blank=True)
    recommendations = models.CharField(max_length=200, null=True, blank=True)
    referred = models.BooleanField(default=False)

    def __str__(self):
        return 'Animal {self.tag}'

class Treatment(models.Model):
    name = models.CharField(max_length=200, null=True)
    cost = models.FloatField()

    def __str__(self):
        return 'Treatment {self.name}'

class Sales(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, default=None)
    status = models.BooleanField(default=False)

    def __str__(self):
        return 'Sales {self.id}'

class Appointment(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, default=None)
    message = models.CharField(max_length=1000, null=True)
    date = models.CharField(max_length=200, null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return 'Appointment {self.id}'



    


