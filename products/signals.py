from django.core.cache import cache
from products.models import Product
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save, pre_save, post_delete


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_delete, sender=Product)
@receiver(pre_save, sender=Product)
@receiver(post_save, sender=Product)
def saved_product(sender, instance, **kwargs):
    category_slug = kwargs.get('slug')
    group_slug = kwargs.get('slug')
    cache.delete(f'product_list_{category_slug}_{group_slug}')
    cache.delete(f'product_detail_{instance.slug}')
