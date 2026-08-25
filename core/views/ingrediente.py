from rest_framework.viewsets import ModelViewSet
from core.models import Ingrediente
from core.serializers import IngredienteSerializer, IngredienteRetrieveSerializer, IngredienteListSerializer


class IngredienteViewSet(ModelViewSet):
    queryset = Ingrediente.objects.all()
    serializer_class = IngredienteSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return IngredienteListSerializer
        elif self.action == 'retrieve':
            return IngredienteRetrieveSerializer
        return IngredienteSerializer