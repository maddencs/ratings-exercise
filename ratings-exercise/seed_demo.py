import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "")
django.setup()

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import IntegrityError

from sample.models import Product

try:
    user = User.objects.create(
        username="demo",
        password=make_password("demo123"),
        is_superuser=True,
        is_staff=True,
        is_active=True,
    )
except IntegrityError as e:
    pass


Product.objects.get_or_create(name="Sample Product 1")
