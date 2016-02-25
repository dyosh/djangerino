from django.db import models

class User(models.Model):
    name = models.CharField(max_length=140)
    email = models.EmailField(max_length=254)
    # password = 
    # password_confirmation = 
    