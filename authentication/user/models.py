from django.db import models

# Create your models here.


class Contact(models.Model):
    contact_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    contact_email = models.EmailField(max_length=254)

    def __str__(self):
        return self.contact_name
