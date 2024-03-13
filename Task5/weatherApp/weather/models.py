from django.db import models

class all_cities(models.Model):
    city_name = models.CharField(max_length = 50)

    def __str__(self):
        return self.city_name

class City(models.Model):
    city_id = models.ForeignKey(all_cities, on_delete=models.CASCADE)
    weather = models.CharField(max_length = 40)
    temp = models.FloatField()
    humidity = models.IntegerField()

    def __str__(self):
        return self.city_id.city_name

