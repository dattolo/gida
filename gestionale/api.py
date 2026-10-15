from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Item
from .serializers import ImportSerializer, ItemSerializer, VenditaSerializer


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

    @action(detail=False, methods=['post'], url_path='import')
    def import_items(self, request):
        """Bulk-create items parsed client-side from an Excel file.

        With replace=true the user's current items are deleted first. All or nothing.
        """
        ser = ImportSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        rows = ser.validated_data['items']
        with transaction.atomic():
            if ser.validated_data['replace']:
                self.get_queryset().delete()
            Item.objects.bulk_create([Item(owner=request.user, **row) for row in rows])
        return Response({'imported': len(rows)}, status=status.HTTP_201_CREATED)
