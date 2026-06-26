from rest_framework.viewsets import ModelViewSet

from core.models import Evento
from core.serializers import EventoSerializer


class EventoViewSet(ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
