from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField(default=0.0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

class OrderEntry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="+")
    count = models.IntegerField(default=0)
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="order_entries")

    def __str__(self):
        return f'{self.product} {self.count}'


class StatusOrder(models.TextChoices):
    INITIAL = "IN", _("Initial")
    COMPLETED = "CO", _("Completed")
    DELIVERED = "DE", _("Delivered")


class Order(models.Model):
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=2, choices=StatusOrder.choices, default=StatusOrder.INITIAL)

    def __str__(self):
        return f'{self.profile} - {self.status}'

    def get_total_price(self):
        return sum(order_entry.product.price * order_entry.count for order_entry in self.order_entries.all())

    def get_products_count(self):
        return sum(order_entry.count for order_entry in self.order_entries.all())

    def get_order_status(self):
        if self.status == StatusOrder.INITIAL:
            return 'INITIAL'
        elif self.status == StatusOrder.COMPLETED:
            return 'COMPLETED'
        elif self.status == StatusOrder.DELIVERED:
            return 'DELIVERED'
        else:
            return 'UNKNOWN'

class Profile(models.Model):
   user: User = models.OneToOneField(User, on_delete=models.CASCADE)
   shopping_cart: Order = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

   def __str__(self):
       return str(self.user)

   @classmethod
   def init_shopping_cart(cls, user: User):
       profile: Profile = Profile.objects.get_or_create(user=user)[0]
       if not profile.shopping_cart:
           profile.shopping_cart = (profile.orders.filter(status=StatusOrder.INITIAL).first()
                                    or Order.objects.create(profile=profile, status=StatusOrder.INITIAL))
           profile.save()

       return profile.shopping_cart
