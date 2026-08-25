from rest_framework.viewsets import ModelViewSet
from core.models import UtensilioEvento
from core.serializers import UtensilioEventoSerializer, UtensilioEventoRetrieveSerializer, UtensilioEventoListSerializer


class UtensilioEventoViewSet(ModelViewSet):
    queryset = UtensilioEvento.objects.all()
    serializer_class = UtensilioEventoSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return UtensilioEventoListSerializer
        elif self.action == 'retrieve':
            return UtensilioEventoRetrieveSerializer
        return UtensilioEventoSerializer