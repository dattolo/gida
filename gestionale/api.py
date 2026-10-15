from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Item
from .serializers import ItemSerializer, VenditaSerializer


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer

    def get_queryset(self):
        # Each user only ever sees their own items; others' ids return 404.
        return Item.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def vendi(self, request, pk=None):
        item = self.get_object()
        ser = VenditaSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        item.vendita_dt = ser.validated_data['vendita_dt']
        item.prezzo_vendita = ser.validated_data['prezzo_vendita']
        item.save()
        return Response(self.get_serializer(item).data)

    @action(detail=True, methods=['post'])
    def annulla_vendita(self, request, pk=None):
        item = self.get_object()
        item.vendita_dt = None
        item.prezzo_vendita = None
        item.save()
        return Response(self.get_serializer(item).data)

    # TODO (P3): export / import_excel actions with openpyxl.
