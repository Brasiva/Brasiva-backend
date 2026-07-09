from rest_framework.viewsets import ModelViewSet

from core.models import Cardapio
from core.serializers import CardapioSerializer


class CardapioViewSet(ModelViewSet):
    queryset = Cardapio.objects.all()
    serializer_class = CardapioSerializer
