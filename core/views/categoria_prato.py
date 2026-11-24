from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from core.permissions import IsStaffOrReadOnly

from core.models import CategoriaPrato
from core.serializers import CategoriaPratoSerializer


class CategoriaPratoViewSet(ModelViewSet):
    queryset = CategoriaPrato.objects.all().order_by('nome')
    serializer_class = CategoriaPratoSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(publicada=True)
        return queryset

    def destroy(self, request, *args, **kwargs):
        categoria = self.get_object()
        if categoria.pratos.exists():
            return Response({'detail': 'Mova ou exclua os produtos da categoria antes de removê-la.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)
