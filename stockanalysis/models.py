from django.db import models

class Stock(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=50) # unique symblol
    sector = models.CharField(max_length=100, null=True, blank=True)
    exchange = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
