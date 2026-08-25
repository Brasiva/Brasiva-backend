from rest_framework.viewsets import ModelViewSet
from core.models import ClienteEvento
from core.serializers import ClienteEventoSerializer, ClienteEventoListSerializer, ClienteEventoRetrieveSerializer


class ClienteEventoViewSet(ModelViewSet):
    queryset = ClienteEvento.objects.all()
    serializer_class = ClienteEventoSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ClienteEventoListSerializer
        elif self.action == 'retrieve':
            return ClienteEventoRetrieveSerializer
        return ClienteEventoSerializer