from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from core.models import Estoque
from core.serializers import EstoqueSerializer


class EstoqueViewSet(ModelViewSet):
    queryset = Estoque.objects.all()
    serializer_class = EstoqueSerializer
    permission_classes = [IsAdminUser]
