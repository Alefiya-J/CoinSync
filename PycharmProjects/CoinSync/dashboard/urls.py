from django.urls import path
from . import views

app_name = "coinsync"

urlpatterns = [
    path(r'',views.index, name="index"),
    path(r'home/',views.landing, name="landing"),
    path(r'conversions/<str:type>/',views.conversions, name="conversions"),
    path(r'trends/<str:crypto>/<str:price>', views.crypto_chart, name="charts"),
    path(r'signup/', views.signup, name='signup'),
    path(r'login/', views.user_login, name='login'),
    path(r'logout/', views.user_logout, name='logout'),
    path(r'contact/', views.contact, name='contact'),
    path(r'feedback/', views.feedback_form, name='feedback'),
    path(r'success/', views.success, name='success'),
    path(r'user/dashboard/', views.dashboard, name='dashboard'),
    path(r'user/dashboard/buy', views.buy_crypto, name='buy'),
    path(r'user/dashboard/sell', views.sell_crypto, name='sell'),
    path(r'user/dashboard/history', views.payment_history, name='history'),
    path(r'user/dashboard/add-balance', views.add_balance, name='balance'),
    path(r'user/dashboard/get-listed', views.crypto_request, name='crypto_request'),
]