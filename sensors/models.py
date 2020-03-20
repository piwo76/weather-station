from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# DHT22: Temperature and humidity sensor
class DHT22(BaseModel):
    temperature = models.FloatField(default=0.0, validators=[MinValueValidator(-50.0), MaxValueValidator(100.0)])
    humidity = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    filtered_temperature = models.FloatField(default=0.0, validators=[MinValueValidator(-50.0), MaxValueValidator(100.0)])
    filtered_humidity = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    valid = models.BooleanField(default=True)
