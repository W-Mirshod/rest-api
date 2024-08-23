from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from products.models import Product


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)

# @receiver(pre_save, sender=Product)
# @receiver(post_save, sender=Product)
# def save_product(sender, instance, **kwargs):
#     instance.de
