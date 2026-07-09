from rest_framework.viewsets import ModelViewSet

from core.models import PratoEvento
from core.serializers import PratoEventoSerializer


class PratoEventoViewSet(ModelViewSet):
    queryset = PratoEvento.objects.all()
    serializer_class = PratoEventoSerializer
