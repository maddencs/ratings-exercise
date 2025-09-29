from venv import create

import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from sample.models import Product, ProductRating


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.mark.django_db
class TestRatingEndpoints:
    @pytest.fixture(autouse=True)
    def init(self, api_client):
        self.api_client = api_client
        self.user = User.objects.create(username='test', password='')
        self.product = Product.objects.create(name='test product')

    def test_product_rating_list(self):
        rating = ProductRating.objects.create(user=self.user, product=self.product, number_rating=1)
        self.api_client.force_authenticate(user=self.user)
        url = reverse('productrating-list')
        response = self.api_client.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]['id'] == rating.id

    def test_rate_product(self):
        self.api_client.force_authenticate(user=self.user)
        data = {
            'product': self.product.id,
            'number_rating': 1,
            'is_liked': True,
        }
        url = reverse('productrating-list')
        response = self.api_client.post(url, data=data)
        assert response.status_code == 201

        created_rating = ProductRating.objects.first()
        assert created_rating.number_rating == 1
        assert created_rating.is_liked
        assert created_rating.user == self.user

    def test_update_product_rating(self):
        self.api_client.force_authenticate(user=self.user)
        rating = ProductRating.objects.create(user=self.user, product=self.product, number_rating=1)
        url = reverse('productrating-detail', kwargs={'pk': rating.id})
        data = {'number_rating': 2}
        response = self.api_client.patch(url, data=data)
        assert response.status_code == 200

        rating.refresh_from_db()
        assert rating.number_rating == 2