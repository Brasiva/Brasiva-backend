from rest_framework.viewsets import ModelViewSet
from core.models import Prato
from core.serializers import PratoSerializer, PratoRetrieveSerializer, PratoListSerializer  


class PratoViewSet(ModelViewSet):
    queryset = Prato.objects.all()
    serializer_class = PratoSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return PratoListSerializer
        elif self.action == 'retrieve':
            return PratoRetrieveSerializer
        return PratoSerializer