from django.db import models

# Create your models here.
class Zad(models.Model):
    sem = models.CharField(max_length=2)
    zad = models.CharField(max_length=10)
    page = models.IntegerField()
    identifier = models.CharField(max_length=10, primary_key=True)

    def __str__(self):
        return self.zad