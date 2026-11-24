from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from core.permissions import IsStaffOrReadOnly

from core.models import Prato
from core.serializers import PratoSerializer, PratoRetrieveSerializer, PratoListSerializer  


class PratoViewSet(ModelViewSet):
    queryset = Prato.objects.select_related('categoria', 'imagem').all().order_by('categoria__nome', 'nome')
    serializer_class = PratoSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return PratoListSerializer
        elif self.action == 'retrieve':
            return PratoRetrieveSerializer
        return PratoSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.method in ('GET', 'HEAD', 'OPTIONS') and not self.request.user.is_staff:
            queryset = queryset.filter(categoria__publicada=True, disponivel=True).filter(Q(valor__isnull=False) | Q(sob_orcamento=True))
        categoria = self.request.query_params.get('categoria')
        return queryset.filter(categoria_id=categoria) if categoria else queryset
