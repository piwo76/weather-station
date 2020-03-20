import datetime

from django.utils import timezone

from sensors.models import DHT22


class DataCollector:
    def current(self):
        current = {}
        dht22_current = DHT22.objects.all().order_by('-id').first()
        current['temperature'] = dht22_current.filtered_temperature
        current['humidity'] = dht22_current.filtered_humidity
        return current

    def last24h(self):
        temperature_last24h = []
        humidity_last24h = []
        start_date = datetime.datetime.now() - datetime.timedelta(days=1)
        now = timezone.now()
        dht22_last24h = DHT22.objects.filter(created_at__gte=start_date, valid=True).order_by('id')
        for measurement in dht22_last24h:
            dtimeh = (now - measurement.created_at).total_seconds() / 3600
            temperature_last24h.append([dtimeh, measurement.filtered_temperature])
            humidity_last24h.append([dtimeh, measurement.filtered_humidity])

        return {'temperature': [temperature_last24h], 'humidity': [humidity_last24h]}

    def lastweek(self):
        return self._get_min_max_last_n_days(7)

    def lastmonth(self):
        return self._get_min_max_last_n_days(30)

    def lastyear(self):
        return self._get_min_max_last_n_days(365)


    def _get_min_max_last_n_days(self, days):
        max_temperature = []
        max_humidity = []
        min_temperature = []
        min_humidity = []
        for day in range(-days, 1):
            start = timezone.now().date() + datetime.timedelta(day);
            day_start = datetime.datetime.combine(start, datetime.time())
            day_end = datetime.datetime.combine(start + datetime.timedelta(1), datetime.time())
            measurements_for_day = DHT22.objects.filter(valid=True, created_at__lte=day_end, created_at__gte=day_start)
            if measurements_for_day:
                max_temp_for_day = measurements_for_day.order_by('-temperature').first().filtered_temperature
                min_temp_for_day = measurements_for_day.order_by('temperature').first().filtered_temperature
                max_humidity_for_day = measurements_for_day.order_by('-humidity').first().filtered_humidity
                min_humidity_for_day = measurements_for_day.order_by('humidity').first().filtered_humidity
                max_temperature.append([day, max_temp_for_day])
                max_humidity.append([day, max_humidity_for_day])
                min_temperature.append([day, min_temp_for_day])
                min_humidity.append([day, min_humidity_for_day])

        return {'max_temperature': [max_temperature], 'min_temperature': [min_temperature],
                'max_humidity': [max_humidity], 'min_humidity': [min_humidity]}