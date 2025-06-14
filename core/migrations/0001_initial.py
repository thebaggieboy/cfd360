# Generated by Django 4.2 on 2025-06-12 23:23

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InvestmentPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(blank=True, max_length=250, null=True)),
                ('amount', models.IntegerField()),
                ('investment_plan', models.CharField(blank=True, max_length=250, null=True)),
                ('investment_duration', models.CharField(blank=True, max_length=250, null=True)),
                ('investment_date', models.DateTimeField(blank=True, max_length=250, null=True)),
                ('status', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=250, null=True)),
                ('expected_return', models.CharField(blank=True, max_length=250, null=True)),
                ('current_value', models.CharField(blank=True, max_length=250, null=True)),
                ('average_return', models.CharField(blank=True, max_length=250, null=True)),
                ('daily_roi', models.CharField(blank=True, max_length=250, null=True)),
                ('weekly_roi', models.CharField(blank=True, max_length=250, null=True)),
                ('monthly_roi', models.CharField(blank=True, max_length=250, null=True)),
                ('daily_interest', models.CharField(blank=True, max_length=250, null=True)),
                ('weekly_interest', models.CharField(blank=True, max_length=250, null=True)),
                ('monthly_interest', models.CharField(blank=True, max_length=250, null=True)),
                ('daily_roi_date', models.DateTimeField(blank=True, max_length=250, null=True)),
                ('weekly_roi_date', models.DateTimeField(blank=True, max_length=250, null=True)),
                ('monthly_roi_date', models.DateTimeField(blank=True, max_length=250, null=True)),
                ('daily_interest_date', models.DateTimeField(blank=True, max_length=250, null=True)),
                ('daily_transactions', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=250, null=True), default=list, size=None)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('amount', models.CharField(blank=True, max_length=100, null=True)),
                ('type', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('transaction_date', models.DateTimeField(blank=True, max_length=250, null=True)),
                ('transaction_id', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('payment_method', models.CharField(blank=True, choices=[('Bank', 'Bank'), ('Crypto', 'Crypto'), ('Card', 'Card')], default='Crypto', max_length=250, null=True)),
                ('crypto_currrency', models.CharField(blank=True, choices=[('Bitcoin', 'Bitcoin'), ('Ethereum', 'Ethereum'), ('USDC', 'USDC'), ('Litecoin', 'Litecoin'), ('Tether', 'Tether'), ('Solana', 'Solana'), ('Tron', 'Tron'), ('Polygon', 'Polygon')], default='Bitcoin', max_length=250, null=True)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Withdraw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(blank=True, max_length=250, null=True)),
                ('withdrawal_method', models.CharField(blank=True, choices=[('Bank', 'Bank'), ('Crypto', 'Crypto')], default='Bitcoin', max_length=250, null=True)),
                ('status', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=250, null=True)),
                ('withdrawal_date', models.DateTimeField(blank=True, max_length=250, null=True)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True)),
                ('user', models.ForeignKey(blank=True, max_length=250, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Wallets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('balance', models.CharField(blank=True, default=0.0, max_length=250, null=True)),
                ('profit_margin', models.FloatField(blank=True, default=0.0, max_length=250, null=True)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True)),
                ('today', models.CharField(blank=True, default=0.0, max_length=250, null=True)),
                ('this_week', models.CharField(blank=True, default=0.0, max_length=250, null=True)),
                ('this_month', models.CharField(blank=True, default=0.0, max_length=250, null=True)),
                ('today_roi', models.CharField(blank=True, default=0.0, max_length=250, null=True)),
                ('this_week_roi', models.CharField(blank=True, default=0.0, max_length=250, null=True)),
                ('this_month_roi', models.CharField(blank=True, default=0.0, max_length=250, null=True)),
                ('all_time_roi', models.CharField(blank=True, default=0.0, max_length=250, null=True)),
                ('date_created', models.DateTimeField(blank=True, max_length=250, null=True)),
                ('transactions', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.transaction')),
                ('user', models.OneToOneField(blank=True, max_length=250, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_charge_id', models.CharField(max_length=50)),
                ('amount', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Deposits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(blank=True, default=0.0, max_length=250, null=True)),
                ('quick_trade', models.CharField(blank=True, max_length=250, null=True)),
                ('payment_method', models.CharField(blank=True, choices=[('Bank', 'Bank'), ('Crypto', 'Crypto')], default='Bitcoin', max_length=250, null=True)),
                ('crypto_currrency', models.CharField(blank=True, choices=[('Bitcoin', 'Bitcoin'), ('Ethereum', 'Ethereum'), ('USDC', 'USDC'), ('Litecoin', 'Litecoin'), ('Tether', 'Tether'), ('Solana', 'Solana'), ('Tron', 'Tron'), ('Polygon', 'Polygon')], default='Bitcoin', max_length=250, null=True)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True)),
                ('status', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=250, null=True)),
                ('date_created', models.DateTimeField(blank=True, max_length=250, null=True)),
                ('user', models.ForeignKey(blank=True, max_length=250, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Banks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(blank=True, default=0.0, max_length=250, null=True)),
                ('bank_address', models.CharField(blank=True, max_length=250, null=True)),
                ('account_number', models.CharField(blank=True, max_length=250, null=True)),
                ('account_name', models.CharField(blank=True, max_length=250, null=True)),
                ('swift_code', models.CharField(blank=True, max_length=250, null=True)),
                ('routing_number', models.CharField(blank=True, max_length=250, null=True)),
                ('state', models.CharField(blank=True, max_length=250, null=True)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True)),
                ('user', models.ForeignKey(blank=True, max_length=250, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(max_length=100)),
                ('apartment_address', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('zip', models.CharField(max_length=100)),
                ('address_type', models.CharField(choices=[('B', 'Billing'), ('S', 'Shipping')], max_length=1)),
                ('default', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Addresses',
            },
        ),
    ]
