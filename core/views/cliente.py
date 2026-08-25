from rest_framework.viewsets import ModelViewSet
from core.models import Cliente
from core.serializers import ClienteSerializer, ClienteRetrieveSerializer, ClienteListSerializer


class ClienteViewSet(ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ClienteListSerializer
        elif self.action == 'retrieve':
            return ClienteRetrieveSerializer
        return ClienteSerializer
