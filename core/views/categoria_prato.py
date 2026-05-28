from rest_framework.viewsets import ModelViewSet

from core.models import CategoriaPrato
from core.serializers import CategoriaPratoSerializer


class CategoriaPratoViewSet(ModelViewSet):
    queryset = CategoriaPrato.objects.all()
    serializer_class = CategoriaPratoSerializer
