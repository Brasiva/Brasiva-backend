from rest_framework.viewsets import ModelViewSet

from core.models import CardapioEvento
from core.serializers import CardapioEventoSerializer


class CardapioEventoViewSet(ModelViewSet):
    queryset = CardapioEvento.objects.all()
    serializer_class = CardapioEventoSerializer
