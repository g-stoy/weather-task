from django.db import models

class City(models.Model):
    city = models.CharField(max_length = 50)
    weather = models.CharField(max_length = 40)
    temp = models.FloatField()
    humidity = models.IntegerField()

    
class all_cities(models.Model):
    city = models.CharField(max_length = 50)

