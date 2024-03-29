# Generated by Django 4.2.7 on 2023-11-27 00:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_alter_usercryptocurrency_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='CryptoRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('symbol', models.CharField(max_length=10)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('circulating_supply', models.DecimalField(decimal_places=2, max_digits=15)),
                ('total_supply', models.DecimalField(decimal_places=2, max_digits=15)),
                ('market_cap', models.DecimalField(decimal_places=2, max_digits=15)),
                ('release_date', models.DateField()),
                ('website', models.URLField(blank=True, null=True)),
                ('whitepaper', models.URLField(blank=True, null=True)),
                ('additional_info', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crypto_requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
