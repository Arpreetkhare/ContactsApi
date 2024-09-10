from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Contact(models.Model):
    contact_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    contact_email = models.EmailField(max_length=254)
    is_fav=models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    Other_details = models.JSONField(default=dict, blank=True)
    shared_with = models.ManyToManyField(User, related_name="shared_contacts", blank=True) 


    def __str__(self):
        return self.contact_name