from rest_framework.viewsets import ModelViewSet

from core.models import Convite
from core.serializers import ConviteSerializer


class ConviteViewSet(ModelViewSet):
    queryset = Convite.objects.all()
    serializer_class = ConviteSerializer
