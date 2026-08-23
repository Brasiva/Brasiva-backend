from rest_framework.viewsets import ModelViewSet

from core.models import ClienteEvento
from core.serializers import ClienteEventoSerializer


class ClienteEventoViewSet(ModelViewSet):
    queryset = ClienteEvento.objects.all()
    serializer_class = ClienteEventoSerializer
