from rest_framework.viewsets import ModelViewSet
from core.models import Funcionario
from core.serializers import FuncionarioSerializer, FuncionarioRetrieveSerializer, FuncionarioListSerializer


class FuncionarioViewSet(ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return FuncionarioListSerializer
        elif self.action == 'retrieve':
            return FuncionarioRetrieveSerializer
        return FuncionarioSerializer