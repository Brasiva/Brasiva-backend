from rest_framework.viewsets import ModelViewSet

from core.models import Evento, Endereco
from core.serializers import EventoSerializer, EnderecoSerializer


class EventoViewSet(ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer

class EnderecoViewSet(ModelViewSet):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer
