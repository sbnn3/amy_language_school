from django.db import models



class Message(models.Model):
    """
    Contact Form Model
    """
    name = models.CharField(max_length=254)
    phone_number = models.IntegerField()
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=254)
    message = models.TextField(max_length=2000)

    def __str__(self):
        return self.name
