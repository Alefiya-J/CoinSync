import requests
import plotly.express as px
import pandas as pd

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm,LoginForm, FilterForm, CurrencyConversionForm, CryptoConversionForm, BuyCryptoForm, SellCryptoForm, AddBalanceForm, ContactForm, CryptoRequestForm, FeedbackForm, NewsletterSubscriptionForm
from dashboard.models import Categories, CurrencyConversion, Currency, CustomUser, Cryptocurrency, PaymentHistory, UserCryptocurrency


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            request.session['user_id'] = user.id
            return redirect('coinsync:index')
        else:
            error = form.errors
            print(form.errors)
            return render(request, 'signup.html', {'form': form, 'error': error})
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            request.session['user_id'] = user.id
            return redirect('coinsync:index')
        else:
            error = form.errors
            print(form.errors)
            return render(request, 'login.html', {'form': form, 'error': error})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def user_logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    logout(request)
    return redirect('coinsync:landing')


def index(request):
    is_user_authenticated = request.user.is_authenticated
    coins = requests.get(
        'https://api.coingecko.com/api/v3/coins/markets?vs_currency=cad&order=market_cap_desc&per_page=30&page=1&sparkline=true')
    trendingCoins = requests.get('https://api.coingecko.com/api/v3/search/trending').json().get("coins")[0:6]
    trendingNfts = requests.get('https://api.coingecko.com/api/v3/search/trending').json().get("nfts")[0:6]
    trendingCategories = Categories.objects.all()
    global_data = requests.get("https://api.coinlore.net/api/global/").json()[0]
    print(coins)
    if coins.status_code // 100 == 4:
        coins = Cryptocurrency.objects.all()
    else:
        coins = coins.json()
    if request.method == 'GET':
        form = FilterForm(request.GET)
        data = {"coins": coins, "trendingCoins": trendingCoins, "trendingNfts": trendingNfts,
                "trendingCategories": trendingCategories, 'is_user_authenticated': is_user_authenticated,
                "form": form, 'global_data': global_data}
        if form.is_valid():
            sortOrder = form.cleaned_data['sortOrder']
            selectedCurrency = form.cleaned_data['currency']
            selectedCategory = form.cleaned_data['category']
            print(sortOrder, selectedCurrency, selectedCategory)
            req = f'https://api.coingecko.com/api/v3/coins/markets?vs_currency={selectedCurrency}&category={selectedCategory}&order=market_cap_{sortOrder}&per_page=20&page=1&sparkline=true'
            coins = requests.get(req)
            if coins.status_code // 100 == 4:
                coins = Cryptocurrency.objects.all()
            else:
                coins = coins.json()
            data = {
                "coins": coins,
                "trendingCoins": trendingCoins,
                "trendingNfts": trendingNfts,
                "trendingCategories": trendingCategories,
                'is_user_authenticated': is_user_authenticated,
                "form": form,
                'global_data': global_data,
            }
            return render(request, 'index.html', data)

    else:
        form = FilterForm()
        print(form.errors)
        data = {
            "coins": coins,
            "trendingCoins": trendingCoins,
            "trendingNfts": trendingNfts,
            "trendingCategories": trendingCategories,
            'is_user_authenticated': is_user_authenticated,
            "form": form,
            'global_data': global_data,
        }
    return render(request, 'index.html',data)

def crypto_chart(request, crypto, price):
    crypto = crypto
    price = [float(p.replace('e', '')) for p in price.split('-')]
    df = pd.DataFrame({'Price': price})

    fig = px.line(df, y='Price', title='Price over Time', labels={'Price': 'Price'}, line_shape='linear')
    plot_html = fig.to_html(full_html=False)

    return render(request, 'crypto_charts.html', {'crypto': crypto, 'price': price, 'chart':plot_html})

def landing(request):
    is_user_authenticated = request.user.is_authenticated
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('coinsync:landing')
    else:
        form = NewsletterSubscriptionForm()
    return render(request, 'landing.html', context={'is_user_authenticated': is_user_authenticated, 'form': form})


def conversions(request, type):
    result = None
    is_user_authenticated = request.user.is_authenticated
    if request.method == 'POST':
        if type == 'Crypto':
            form = CryptoConversionForm(request.POST)
        else:
            form = CurrencyConversionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            from_currency = form.cleaned_data['from_currency']
            to_currency = form.cleaned_data['to_currency']

            conversion = CurrencyConversion.objects.get(
                from_currency=from_currency,
                to_currency=to_currency
            )
            currency = Currency.objects.get(code=to_currency)
            result = amount * conversion.rate
            return render(request, 'convertor.html', {'form': form, 'result': result, 'type': type, 'is_user_authenticated': is_user_authenticated})

    else:
        if type == 'Crypto':
            form = CryptoConversionForm(request.POST)
        else:
            form = CurrencyConversionForm(request.POST)

    return render(request, 'convertor.html', {'form': form, 'result': result, 'type': type, 'is_user_authenticated': is_user_authenticated})


@login_required(login_url="/home")
def dashboard(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(CustomUser, id=user_id)
    cryptos = UserCryptocurrency.objects.filter(user = user)[0:4]
    data = {
        'Cryptocurrency': [crypto.cryptocurrency.name for crypto in cryptos],
        'Quantity': [crypto.quantity for crypto in cryptos],
    }

    df = pd.DataFrame(data)

    fig = px.pie(df, names='Cryptocurrency', values='Quantity', title='User Cryptocurrency Assets')

    chart = fig.to_html(full_html=False)

    return render(request, 'user-profile.html', context={'user':user, 'cryptos': cryptos, 'chart': chart})


@login_required(login_url="/home")
def buy_crypto(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = BuyCryptoForm(user, request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cryptocurrency = form.cleaned_data['cryptocurrency']
            crypto = Cryptocurrency.objects.get(name__iexact=cryptocurrency)
            total_cost = quantity * crypto.current_price
            if user.balance >= total_cost:
                user.balance -= total_cost
                user.save()
                form.save()

                PaymentHistory.objects.create(
                    user=user,
                    transaction_type='Cryptocurrency Purchase',
                    amount=total_cost,
                    cryptocurrency=crypto,
                )

                return redirect('coinsync:dashboard')
            else:
                messages = 'Insufficient balance for the purchase. Add balance to your wallet.'
                return render(request, 'buy_crypto.html', {'form': form, 'message': messages})
    else:
        form = BuyCryptoForm(user)

    return render(request, 'buy_crypto.html', {'form': form})


@login_required(login_url="/home")
def sell_crypto(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = SellCryptoForm(user, request.POST)
        if form.is_valid():
            cryptocurrency = form.cleaned_data['cryptocurrency']
            crypto = Cryptocurrency.objects.get(name__iexact=cryptocurrency)
            amount_sold = form.cleaned_data['amount_sold']
            quantity = form.cleaned_data['quantity']
            user_crypto = UserCryptocurrency.objects.get(user=user, cryptocurrency=crypto)
            if user_crypto.quantity >= quantity:
                crypto = user_crypto.cryptocurrency

                user_crypto.amount_bought -= quantity*crypto.current_price
                user_crypto.quantity -= quantity
                print(user_crypto.quantity, quantity)
                user_crypto.save()

                user.balance += amount_sold
                user.save()
                PaymentHistory.objects.create(
                    user=user,
                    transaction_type='Cryptocurrency Sale',
                    amount=amount_sold,
                    cryptocurrency=crypto,
                )

                return redirect('coinsync:dashboard')
            else:
                messages = 'Insufficient cryptocurrency for the sale.'
                return render(request, 'sell_crypto.html', {'form': form, 'message': messages})

    else:
        form = SellCryptoForm(user)

    return render(request, 'sell_crypto.html', {'form': form})


@login_required(login_url="/home")
def add_balance(request):
    user_id = request.session.get('user_id')
    print(user_id)
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = AddBalanceForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']

            PaymentHistory.objects.create(
                user=user,
                transaction_type='Wallet Top-Up',
                amount=amount,
            )

            user.balance += amount
            user.save()

            return redirect('coinsync:dashboard')
        else:
            messages = 'Invalid form data. Please check the entered information.'
            return render(request, 'add_balance.html', {'form': form, 'message': messages})

    else:
        form = AddBalanceForm()

    return render(request, 'add_balance.html', {'form': form})


@login_required(login_url="/home")
def payment_history(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(CustomUser, id=user_id)
    history = PaymentHistory.objects.filter(user=user).order_by('-transaction_date')

    return render(request, 'payment_history.html', {'payment_history': history})


def contact(request):
    is_user_authenticated = request.user.is_authenticated
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            return render(request, template_name='success.html', context={'message': 'We\'ll get back to you soon', "is_user_authenticated": is_user_authenticated})
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form, "is_user_authenticated": is_user_authenticated})


def crypto_request(request):
    is_user_authenticated = request.user.is_authenticated
    if request.method == 'POST':
        form = CryptoRequestForm(request.POST)
        if form.is_valid():
            request_data = form.save(commit=False)
            user_id = request.session.get('user_id')
            request_data.user = get_object_or_404(CustomUser, id=user_id)
            request_data.save()
            return render(request, template_name='success.html', context={'message': 'Crypto request submitted. We\'ll keep you updated', "is_user_authenticated": is_user_authenticated})
    else:
        form = CryptoRequestForm()

    return render(request, 'crypto_request.html', {'form': form, 'is_user_authenticated': is_user_authenticated})


def feedback_form(request):
    is_user_authenticated = request.user.is_authenticated
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, template_name='success.html', context={'message': 'Thank you giving us your valuable feedback', "is_user_authenticated": is_user_authenticated})
    else:
        form = FeedbackForm()

    return render(request, 'feedback_form.html', {'form': form, 'is_user_authenticated': is_user_authenticated})


def success(request):
    return render(request, template_name='success.html', context={'message': 'You\'re on success page'})


def subscribe_newsletter(request):
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thank_you_page')
    else:
        form = NewsletterSubscriptionForm()

    return render(request, 'subscribe_newsletter.html', {'form': form})