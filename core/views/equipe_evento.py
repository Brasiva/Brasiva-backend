from rest_framework.viewsets import ModelViewSet
from core.models import EquipeEvento
from core.serializers import EquipeEventoSerializer, EquipeEventoListSerializer, EquipeEventoRetrieveSerializer


class EquipeEventoViewSet(ModelViewSet):
    queryset = EquipeEvento.objects.all()
    serializer_class = EquipeEventoSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return EquipeEventoListSerializer
        elif self.action == 'retrieve':
            return EquipeEventoRetrieveSerializer
        return EquipeEventoSerializer