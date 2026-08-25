from rest_framework.viewsets import ModelViewSet
from core.models import ItemCompra
from core.serializers import ItemCompraSerializer, ItemCompraRetrieveSerializer, ItemCompraListSerializer


class ItemCompraViewSet(ModelViewSet):
    queryset = ItemCompra.objects.all()
    serializer_class = ItemCompraSerializer


    def get_serializer_class(self):
        if self.action == 'list':
            return ItemCompraListSerializer
        elif self.action == 'retrieve':
            return ItemCompraRetrieveSerializer
        return ItemCompraSerializer