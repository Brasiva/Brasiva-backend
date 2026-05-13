from rest_framework.viewsets import ModelViewSet

from core.models import Utensilio
from core.serializers import UtensilioSerializer


class UtensilioViewSet(ModelViewSet):
    queryset = Utensilio.objects.all()
    serializer_class = UtensilioSerializer
