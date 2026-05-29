from rest_framework.viewsets import ModelViewSet

from core.models import IngredientePrato
from core.serializers import IngredientePratoSerializer


class IngredientePratoViewSet(ModelViewSet):
    queryset = IngredientePrato.objects.all()
    serializer_class = IngredientePratoSerializer
