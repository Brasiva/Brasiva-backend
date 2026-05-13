from rest_framework.viewsets import ModelViewSet

from core.models import TipoEvento
from core.serializers import TipoEventoSerializer


class TipoEventoViewSet(ModelViewSet):
    queryset = TipoEvento.objects.all()
    serializer_class = TipoEventoSerializer
