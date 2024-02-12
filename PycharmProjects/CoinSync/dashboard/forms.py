# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Categories, Currency, Cryptocurrency, UserCryptocurrency, CryptoRequest, Feedback, NewsletterSubscription


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'data-toggle': 'tooltip',
                                      'title': 'Letters, digits and @/./+/-/_ only.'})
    )

    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(),
        label= "Password"
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        strip=False,
        label="Confirm Password"
    )

    full_name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    id_proof = forms.ImageField(required=True)

    class Meta:
        model = CustomUser
        fields = [ 'full_name', 'email', 'phone_number','username', 'password1', 'password2', 'id_proof']



class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class FilterForm(forms.Form):
    SORT_CHOICES = [
        ('asc', 'Ascending'),
        ('desc', 'Descending'),
    ]

    CURRENCY_CHOICES = [(currency.code.lower(), currency.code) for currency in Currency.objects.all().order_by('code')]
    CATEGORY_CHOICES = [(category.name.lower(), category.name) for category in Categories.objects.all().order_by('name')]

    sortOrder = forms.ChoiceField(label='Sort Order', choices=SORT_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    currency = forms.ChoiceField(label='Select Currency', choices=CURRENCY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    category = forms.ChoiceField(label='Select Category', choices=CATEGORY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))


class CurrencyConversionForm(forms.Form):
    CURRENCY_CHOICES = [(currency.code, currency.code) for currency in Currency.objects.all().order_by('code')]

    amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2)
    from_currency = forms.ChoiceField(label='From Currency', choices=CURRENCY_CHOICES)
    to_currency = forms.ChoiceField(label='To Currency', choices=CURRENCY_CHOICES)


class CryptoConversionForm(forms.Form):
    CURRENCY_CHOICES = [(currency.code, currency.code) for currency in Currency.objects.all().order_by('code')]
    CRYPTO_CHOICES = [(crypto.name, crypto.name) for crypto in Cryptocurrency.objects.all().order_by('name')]

    amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2)
    from_currency = forms.ChoiceField(label='From Currency', choices=CRYPTO_CHOICES)
    to_currency = forms.ChoiceField(label='To Currency', choices=CURRENCY_CHOICES)


class BuyCryptoForm(forms.Form):
    CRYPTO_CHOICES = [(crypto.name, crypto.name) for crypto in Cryptocurrency.objects.all().order_by('name')]

    quantity = forms.IntegerField(max_value=1000)
    cryptocurrency = forms.ChoiceField(label='Cryptocurrency', choices=CRYPTO_CHOICES)

    def __init__(self, user, *args, **kwargs):
        super(BuyCryptoForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_amount_bought(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("Quantity bought must be greater than zero.")
        return quantity

    def save(self):
        crypto_name = self.cleaned_data['cryptocurrency']
        cryptocurrency = Cryptocurrency.objects.get(name=crypto_name)
        quantity = self.cleaned_data['quantity']

        user_crypto, created = UserCryptocurrency.objects.get_or_create(
            user=self.user,
            cryptocurrency=cryptocurrency,
            defaults={'amount_bought': 0, 'quantity': 0}
        )

        user_crypto.quantity += quantity
        user_crypto.amount_bought += quantity * cryptocurrency.current_price
        user_crypto.save()

        return user_crypto


class AddBalanceForm(forms.Form):
    cardholder_name = forms.CharField(max_length=255, label="Cardholder's Name")
    payment_method = forms.ChoiceField(choices=[('credit_card', 'Credit Card'), ('debit_card', 'Debit Card')], label='Payment Method')
    amount = forms.DecimalField(min_value=1, max_digits=10, decimal_places=2)
    card_number = forms.CharField(max_length=16, label='Card Number', widget=forms.TextInput(attrs={'placeholder': 'XXXX-XXXX-XXXX-XXXX'}))
    expiration_date = forms.CharField(label='Expiration Date', widget=forms.TextInput(attrs={'placeholder': 'MM/YYYY'}))
    cvv = forms.CharField(max_length=3, label='CVV', widget=forms.TextInput(attrs={'placeholder': 'XXX'}))


class SellCryptoForm(forms.Form):
    quantity = forms.IntegerField(max_value=1000)
    amount_sold = forms.DecimalField(min_value=0.001, max_digits=10, decimal_places=3)
    cryptocurrency = forms.ChoiceField(label='Cryptocurrency')

    def __init__(self, user, *args, **kwargs):
        super(SellCryptoForm, self).__init__(*args, **kwargs)

        self.fields['cryptocurrency'].choices = [
            (crypto.cryptocurrency, crypto.cryptocurrency.name)
            for crypto in UserCryptocurrency.objects.filter(user=user)
        ]


class ContactForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label='Your Email', max_length=100)
    message = forms.CharField(label='Your Message', widget=forms.Textarea(attrs={'rows': 3}))


class CryptoRequestForm(forms.ModelForm):
    class Meta:
        model = CryptoRequest
        exclude = ['user', 'status']

    name = forms.CharField(
        max_length=100,
        label='Name',
        help_text='Enter the name of the cryptocurrency.'
    )

    symbol = forms.CharField(
        max_length=10,
        label='Symbol',
        help_text='Enter the symbol of the cryptocurrency.'
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2}),
        label='Description',
        help_text='Provide a brief description of the cryptocurrency.'
    )

    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label='Price',
        help_text='Enter the price of the cryptocurrency.'
    )

    circulating_supply = forms.DecimalField(
        max_digits=15,
        decimal_places=2,
        label='Circulating Supply',
        help_text='Enter the circulating supply of the cryptocurrency.'
    )

    total_supply = forms.DecimalField(
        max_digits=15,
        decimal_places=2,
        label='Total Supply',
        help_text='Enter the total supply of the cryptocurrency.'
    )

    market_cap = forms.DecimalField(
        max_digits=15,
        decimal_places=2,
        label='Market Cap',
        help_text='Enter the market cap of the cryptocurrency.'
    )

    release_date = forms.DateField(
        label='Release Date',
        help_text='Enter the release date of the cryptocurrency.'
    )

    website = forms.URLField(
        required=False,
        label='Website',
        help_text='Provide the URL of the cryptocurrency\'s website if available.'
    )

    whitepaper = forms.URLField(
        required=False,
        label='Whitepaper',
        help_text='Provide the URL of the cryptocurrency\'s whitepaper if available.'
    )

    additional_info = forms.CharField(
        widget=forms.Textarea(attrs={'rows':2}),
        required=False,
        label='Additional Info',
        help_text='Provide any additional information about the cryptocurrency.'
    )


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows':4})
        }


class NewsletterSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "Recipient's email"})
        }

