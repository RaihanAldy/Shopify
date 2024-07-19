from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    STATE_CHOICES = [
        ('disabled', 'disabled'),
        ('invited', 'invited'),
        ('enabled', 'enabled'),
        ('declined', 'declined')
    ]

    user = models.ForeignKey(User, on_delete=models.RESTRICT, unique=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    verified_email = models.BooleanField(default=False)
    send_email_welcome = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='disabled')
    currency = models.CharField(max_length=10)

    @property
    def order_counts(self):
        return 0

class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address1 = models.TextField()
    address2 = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=250)
    province = models.CharField(max_length=250)
    country = models.CharField(max_length=250)
    phone = models.CharField(max_length=100, null=True, blank=True)
    zip = models.CharField(max_length=20)
    company = models.CharField(max_length=200)
    default = models.BooleanField(default=False)

    @property
    def name(self):
        return f"{self.customer.user.first_name} {self.customer.user.last_name}"

class Metafield(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    key = models.CharField(max_length=64)
    namespace = models.CharField(max_length=255)
    owner_id = models.BigIntegerField(unique=True)
    owner_resource = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    value = models.TextField()
    type = models.CharField(max_length=255)

    def _str_(self):
        return f'{self.namespace}:{self.key}'

    class Meta:
        unique_together = ('namespace', 'key', 'owner_id', 'owner_resource')
        
class Collect(models.Model):
    collection_id = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    collect_id = models.BigIntegerField() 
    position = models.CharField(max_length=255)
    product_id = models.BigIntegerField(unique=True) 
    sort_value = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    