from django.db.models import Count, Avg, DecimalField
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from sample.models import ProductRating, Product
from sample.serializers import ProductRatingSerializer, ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().annotate(
        num_ratings=Count('ratings'),
        average_rating=Avg('ratings__number_rating', output_field=DecimalField()),
    ).order_by('-average_rating')
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer


class ProductRatingViewSet(ModelViewSet):
    queryset = ProductRating.objects.all()
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductRatingSerializer
