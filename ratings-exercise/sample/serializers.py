from rest_framework import serializers

from sample.models import ProductRating, Product


class ProductRatingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProductRating
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    average_rating = serializers.DecimalField(
        max_digits=2, decimal_places=1, read_only=True
    )
    num_ratings = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
