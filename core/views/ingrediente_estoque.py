from rest_framework.viewsets import ModelViewSet

from core.models import IngredienteEstoque
from core.serializers import IngredienteEstoqueSerializer


class IngredienteEstoqueViewSet(ModelViewSet):
    queryset = IngredienteEstoque.objects.all()
    serializer_class = IngredienteEstoqueSerializer
