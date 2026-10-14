from rest_framework.serializers import ModelSerializer

from core.models import Evento
from rest_framework import serializers
from django.utils import timezone


class EventoSerializer(ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'

    def validate_quantidade_pessoas(self, value):
        if value <= 0:
            raise serializers.ValidationError("A quantidade de pessoas deve ser maior que zero.")
        return value

    def validate_taxa_utensilio(self, value):
        if value < 0:
            raise serializers.ValidationError("A taxa de utensílio não pode ser negativa.")
        return value

    def validate_taxa_deslocamento(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("A taxa de deslocamento não pode ser negativa.")
        return value

    def validate_data_hora(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("A data e hora do evento não pode ser no passado.")
        return value

    def validate(self, data):
        if 'endereco' not in data or data['endereco'] is None:
            raise serializers.ValidationError({"endereco": "O endereço do evento é obrigatório."})
        if 'tipo_evento' not in data or data['tipo_evento'] is None:
            raise serializers.ValidationError({"tipo_evento": "O tipo de evento é obrigatório."})
        return data

class EventoListSerializer(ModelSerializer):
    class Meta:
        model = Evento
        fields = ('id', 'data_hora', 'local', 'tipo_evento', 'endereco', 'status')

class EventoRetrieveSerializer(ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'
        depth = 1
