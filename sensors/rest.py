from rest_framework import viewsets
from rest_framework.response import Response

from sensors.models import DHT22
from sensors.serializers import DHT22Serializer
from rest_framework.views import APIView

from sensors.services import DataCollector


class DHT22ViewSet(viewsets.ModelViewSet):
    queryset = DHT22.objects.all().order_by('created_at')
    serializer_class = DHT22Serializer


class CurrentView(APIView):
    def get(self, request):
        collector = DataCollector()
        return Response(status=200, data=collector.current())


class HistoryView(APIView):
    def get(self, request):
        history = {}
        collector = DataCollector()
        history['last24h'] = collector.last24h()
        history['lastweek'] = collector.lastweek()
        history['lastmonth'] = collector.lastmonth()
        history['lastyear'] = collector.lastyear()
        return Response(status=200, data=history)
