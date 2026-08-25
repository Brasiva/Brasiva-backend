from rest_framework.viewsets import ModelViewSet
from core.models import Compra
from core.serializers import CompraSerializer, CompraRetrieveSerializer, CompraListSerializer


class CompraViewSet(ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return CompraListSerializer
        elif self.action == 'retrieve':
            return CompraRetrieveSerializer
        return CompraSerializer