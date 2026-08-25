from rest_framework.viewsets import ModelViewSet
from core.models import IngredientePrato
from core.serializers import IngredientePratoSerializer, IngredientePratoRetrieveSerializer, IngredientePratoListSerializer


class IngredientePratoViewSet(ModelViewSet):
    queryset = IngredientePrato.objects.all()
    serializer_class = IngredientePratoSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return IngredientePratoListSerializer
        elif self.action == 'retrieve':
            return IngredientePratoRetrieveSerializer
        return IngredientePratoSerializer