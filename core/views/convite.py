from rest_framework.viewsets import ModelViewSet
from core.models import Convite
from core.serializers import ConviteSerializer, ConviteRetrieveSerializer, ConviteListSerializer


class ConviteViewSet(ModelViewSet):
    queryset = Convite.objects.all()
    serializer_class = ConviteSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ConviteListSerializer
        elif self.action == 'retrieve':
            return ConviteRetrieveSerializer
        return ConviteSerializer