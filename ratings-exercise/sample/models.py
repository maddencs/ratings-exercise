from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import UniqueConstraint


class Product(models.Model):
    name = models.CharField(max_length=100)


class DishType(models.Model):
    name = models.CharField(max_length=100)


class Recipe(models.Model):
    name = models.CharField(max_length=100)


class BaseRating(models.Model):
    """
    Q: Why different tables instead of generic keys?
    A: The different ratings models may change for different reasons. E.g. Recipe/Product may later gain a `review` field
        but DishType would not. It also allows for clear db level constraints and limits migrations to only affecting
        their domain
    """

    number_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    is_liked = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ProductRating(BaseRating):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="ratings",
    )
    user = models.ForeignKey(
        User,
        related_name="product_ratings",
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=["product", "user"], name="unique_product_rating")
        ]


class DishTypeRating(BaseRating):
    dish_type = models.ForeignKey(
        DishType,
        on_delete=models.CASCADE,
        related_name="ratings",
    )
    user = models.ForeignKey(
        User,
        related_name="dish_type_ratings",
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["dish_type", "user"], name="unique_dish_type_dish_rating"
            )
        ]


class RecipeRating(BaseRating):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ratings",
    )
    user = models.ForeignKey(
        User,
        related_name="recipe_ratings",
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=["recipe", "user"], name="unique_recipe_rating")
        ]
