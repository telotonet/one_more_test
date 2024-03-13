from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model


User = get_user_model()


class Event(models.Model):
    title       = models.CharField(max_length=100)
    description = models.TextField()
    organizations = models.ManyToManyField("Organization")
    image       = models.ImageField(upload_to='events/', null=True, blank=True)
    date        = models.DateTimeField()

    def __str__(self):
        return self.title
    

class Organization(models.Model):
    title       = models.CharField(max_length=100)
    description = models.TextField()
    address     = models.CharField(max_length=200)
    postcode    = models.CharField(max_length=10)
    members     = models.ManyToManyField(User, related_name='organizations', blank=True)

    def __str__(self):
        return self.title