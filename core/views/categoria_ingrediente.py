from rest_framework.viewsets import ModelViewSet

from core.models import CategoriaIngrediente
from core.serializers import CategoriaIngredienteSerializer


class CategoriaIngredienteViewSet(ModelViewSet):
    queryset = CategoriaIngrediente.objects.all()
    serializer_class = CategoriaIngredienteSerializer
