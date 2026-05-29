from rest_framework.viewsets import ModelViewSet

from core.models import UtensilioEvento
from core.serializers import UtensilioEventoSerializer


class UtensilioEventoViewSet(ModelViewSet):
    queryset = UtensilioEvento.objects.all()
    serializer_class = UtensilioEventoSerializer
