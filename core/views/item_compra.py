from rest_framework.viewsets import ModelViewSet

from core.models import ItemCompra
from core.serializers import ItemCompraSerializer


class ItemCompraViewSet(ModelViewSet):
    queryset = ItemCompra.objects.all()
    serializer_class = ItemCompraSerializer
