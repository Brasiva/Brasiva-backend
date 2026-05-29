from rest_framework.viewsets import ModelViewSet

from core.models import OrcamentoEvento
from core.serializers import OrcamentoEventoSerializer


class OrcamentoEventoViewSet(ModelViewSet):
    queryset = OrcamentoEvento.objects.all()
    serializer_class = OrcamentoEventoSerializer
