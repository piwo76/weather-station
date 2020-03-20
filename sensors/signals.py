from statistics import median

from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver

from sensors.models import DHT22


@receiver(post_save, sender=DHT22)
def calculated_filtered_signals(sender, instance, raw, created, *args, **kwargs):
    if DHT22.objects.count() > 3:
        measurements = DHT22.objects.filter().order_by('-id')
        last3_temperature = [measurements[2].temperature, measurements[1].temperature, measurements[0].temperature]
        instance.filtered_temperature = median(last3_temperature)
        last3_humidity = [measurements[2].humidity, measurements[1].humidity, measurements[0].humidity]
        instance.filtered_humidity = median(last3_humidity)

        if abs(instance.temperature - instance.filtered_temperature) > 10 or abs(instance.humidity - instance.filtered_humidity) > 20:
            instance.valid = False
    else:
        instance.filtered_temperature = instance.temperature
        instance.filtered_humidity = instance.humidity

    signals.post_save.disconnect(calculated_filtered_signals, sender=DHT22)
    instance.save()
    signals.post_save.connect(calculated_filtered_signals, sender=DHT22)

