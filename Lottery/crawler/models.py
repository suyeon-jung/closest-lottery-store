from django.db import models

# Create your models here.

class LotteryList(models.Model):
    store_name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    lottery_count = models.IntegerField(default=0)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    def __str__(self):
        return self.store_name
    class Meta:
        db_table = 'lottery_store'

