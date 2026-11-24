from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from core.models import CategoriaIngrediente
from core.serializers import CategoriaIngredienteSerializer


class CategoriaIngredienteViewSet(ModelViewSet):
    queryset = CategoriaIngrediente.objects.all()
    serializer_class = CategoriaIngredienteSerializer
    permission_classes = [IsAdminUser]
