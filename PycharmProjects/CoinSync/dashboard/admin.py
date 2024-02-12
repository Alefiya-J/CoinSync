from django.contrib import admin
from .models import CustomUser, Categories, Currency, Cryptocurrency, CurrencyConversion, PaymentHistory, UserCryptocurrency, CryptoRequest, Feedback, NewsletterSubscription
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Categories)
admin.site.register(Currency)
admin.site.register(Cryptocurrency)
admin.site.register(CurrencyConversion)
admin.site.register(PaymentHistory)
admin.site.register(UserCryptocurrency)
admin.site.register(CryptoRequest)
admin.site.register(Feedback)
admin.site.register(NewsletterSubscription)
