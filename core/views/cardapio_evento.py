from rest_framework.viewsets import ModelViewSet

from core.models import CardapioEvento
from core.serializers import CardapioEventoSerializer, CardapioEventoRetrieveSerializer, CardapioEventoListSerializer


class CardapioEventoViewSet(ModelViewSet):
    queryset = CardapioEvento.objects.all()
    serializer_class = CardapioEventoSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return CardapioEventoListSerializer
        elif self.action == 'retrieve':
            return CardapioEventoRetrieveSerializer
        return CardapioEventoSerializer
