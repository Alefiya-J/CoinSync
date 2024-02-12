# models.py

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    id_proof = models.ImageField(upload_to='id_proofs/', blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True)

    def __str__(self):
        return self.username


class Categories(models.Model):
    name = models.CharField(max_length=512)
    image = models.CharField(max_length=512)
    market_cap = models.DecimalField(max_digits=20, decimal_places=2)
    market_cap_change_24h = models.DecimalField(max_digits=20, decimal_places=2)
    content = models.TextField()
    coin1 = models.CharField(max_length=512)
    coin2 = models.CharField(max_length=512)
    coin3 = models.CharField(max_length=512)
    volume_24h = models.DecimalField(max_digits=20, decimal_places=2)


    def __str__(self):
        return self.name


class Cryptocurrency(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=255)
    current_price = models.DecimalField(max_digits=10, decimal_places=5)
    market_cap = models.BigIntegerField()
    market_cap_rank = models.IntegerField()
    total_volume = models.BigIntegerField()
    price_change_percentage_24h = models.DecimalField(max_digits=10, decimal_places=5)

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=3, unique=True)
    symbol = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class CurrencyConversion(models.Model):
    from_currency = models.CharField(max_length=50)
    to_currency = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=20, decimal_places=5)

    def __str__(self):
        return f"{self.from_currency} to {self.to_currency} - Rate: {self.rate}"


class UserCryptocurrency(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    cryptocurrency = models.ForeignKey('Cryptocurrency', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    amount_bought = models.DecimalField(max_digits=20, decimal_places=5)
    date_bought = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bought {self.quantity} {self.cryptocurrency.name} on {self.date_bought}"


class PaymentHistory(models.Model):
    TRANSACTION_CHOICES = [
        ('Cryptocurrency Purchase', 'Cryptocurrency Purchase'),
        ('Cryptocurrency Sale', 'Cryptocurrency Sale'),
        ('Wallet Top-Up', 'Wallet Top-Up'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}  - {self.transaction_date}"


class CryptoRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='crypto_requests')
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    circulating_supply = models.DecimalField(max_digits=15, decimal_places=2)
    total_supply = models.DecimalField(max_digits=15, decimal_places=2)
    market_cap = models.DecimalField(max_digits=15, decimal_places=2)
    release_date = models.DateField()
    website = models.URLField(blank=True, null=True)
    whitepaper = models.URLField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.name


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f'Feedback by {self.name}'


class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email
