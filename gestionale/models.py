from django.conf import settings
from django.db import models


class Item(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='items')
    acquisto_dt = models.DateTimeField('data acquisto')
    descrizione = models.CharField(max_length=255)
    prezzo_acquisto = models.DecimalField(max_digits=10, decimal_places=2)
    vendita_dt = models.DateTimeField('data vendita', null=True, blank=True)
    prezzo_vendita = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-acquisto_dt']
        verbose_name = 'oggetto'
        verbose_name_plural = 'oggetti'

    def __str__(self):
        return self.descrizione

    @property
    def venduto(self):
        return self.prezzo_vendita is not None
