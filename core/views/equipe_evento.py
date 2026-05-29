from rest_framework.viewsets import ModelViewSet

from core.models import EquipeEvento
from core.serializers import EquipeEventoSerializer


class EquipeEventoViewSet(ModelViewSet):
    queryset = EquipeEvento.objects.all()
    serializer_class = EquipeEventoSerializer
