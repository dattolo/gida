from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Item

User = get_user_model()


class ItemApiTests(APITestCase):
    def setUp(self):
        self.ida = User.objects.create_user('ida', password='pw-ida-123')
        self.altro = User.objects.create_user('altro', password='pw-altro-123')
        self.item = Item.objects.create(owner=self.ida, acquisto_dt='2026-10-14T10:00:00+02:00',
                                        descrizione='Lampada', prezzo_acquisto='25.00')

    def test_anonymous_forbidden(self):
        r = self.client.get(reverse('item-list'))
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_home_redirects_to_login(self):
        r = self.client.get(reverse('home'))
        self.assertRedirects(r, reverse('login') + '?next=/')

    def test_list_only_own_items(self):
        self.client.force_authenticate(self.altro)
        self.assertEqual(self.client.get(reverse('item-list')).json(), [])
        r = self.client.get(reverse('item-detail', args=[self.item.pk]))
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_sets_owner(self):
        self.client.force_authenticate(self.altro)
        r = self.client.post(reverse('item-list'), {'acquisto_dt': '2026-10-15T09:00:00+02:00',
                                                    'descrizione': 'Vaso', 'prezzo_acquisto': '10.50'})
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.get(pk=r.json()['id']).owner, self.altro)

    def test_sell_and_unsell(self):
        self.client.force_authenticate(self.ida)
        r = self.client.post(reverse('item-vendi', args=[self.item.pk]),
                             {'vendita_dt': '2026-10-15T12:00:00+02:00', 'prezzo_vendita': '40.00'})
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()['utile'], '15.00')
        r = self.client.post(reverse('item-annulla-vendita', args=[self.item.pk]))
        self.assertIsNone(r.json()['prezzo_vendita'])

    def test_sale_fields_must_go_together(self):
        self.client.force_authenticate(self.ida)
        r = self.client.patch(reverse('item-detail', args=[self.item.pk]), {'prezzo_vendita': '40.00'})
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
