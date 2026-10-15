from rest_framework import serializers

from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    utile = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['id', 'acquisto_dt', 'descrizione', 'prezzo_acquisto',
                  'vendita_dt', 'prezzo_vendita', 'utile']

    def get_utile(self, obj):
        if obj.prezzo_vendita is None:
            return None
        return str(obj.prezzo_vendita - obj.prezzo_acquisto)

    def validate_prezzo_acquisto(self, value):
        if value < 0:
            raise serializers.ValidationError('Il prezzo non può essere negativo.')
        return value

    def validate_prezzo_vendita(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError('Il prezzo non può essere negativo.')
        return value

    def validate(self, data):
        pv = data.get('prezzo_vendita', getattr(self.instance, 'prezzo_vendita', None))
        vd = data.get('vendita_dt', getattr(self.instance, 'vendita_dt', None))
        if (pv is None) != (vd is None):
            raise serializers.ValidationError('Prezzo e data di vendita vanno indicati insieme.')
        return data


class VenditaSerializer(serializers.Serializer):
    vendita_dt = serializers.DateTimeField()
    prezzo_vendita = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)
