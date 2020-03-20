from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from sensors import rest

router = routers.DefaultRouter()
router.register(r'dht22', rest.DHT22ViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^current/$', rest.CurrentView.as_view()),
    url(r'^history/$', rest.HistoryView.as_view()),
]