from rest_framework.viewsets import ModelViewSet

from core.models import Prato
from core.serializers import PratoSerializer


class PratoViewSet(ModelViewSet):
    queryset = Prato.objects.all()
    serializer_class = PratoSerializer
