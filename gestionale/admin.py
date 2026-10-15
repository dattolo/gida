from django.contrib import admin

from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['descrizione', 'owner', 'acquisto_dt', 'prezzo_acquisto', 'vendita_dt', 'prezzo_vendita']
    list_filter = ['owner']
    search_fields = ['descrizione']
    date_hierarchy = 'acquisto_dt'
