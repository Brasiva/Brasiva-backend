from rest_framework.viewsets import ModelViewSet
from core.models import OrcamentoEvento
from core.serializers import OrcamentoEventoSerializer, OrcamentoEventoRetrieveSerializer, OrcamentoEventoListSerializer


class OrcamentoEventoViewSet(ModelViewSet):
    queryset = OrcamentoEvento.objects.all()
    serializer_class = OrcamentoEventoSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return OrcamentoEventoListSerializer
        elif self.action == 'retrieve':
            return OrcamentoEventoRetrieveSerializer
        return OrcamentoEventoSerializer
