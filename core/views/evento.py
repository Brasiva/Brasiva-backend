from rest_framework.viewsets import ModelViewSet
from core.models import Evento
from core.serializers import EventoSerializer, EventoRetrieveSerializer, EventoListSerializer


class EventoViewSet(ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return EventoListSerializer
        elif self.action == 'retrieve':
            return EventoRetrieveSerializer
        return EventoSerializer