# Generated by Django 5.1.7 on 2025-03-21 18:12

import django.db.models.deletion
import django_countries.fields
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('os_project', '0001_initial'),
        ('user_profile', '0002_contributionfocusos_contributionfocuswit_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmation_number', models.CharField(editable=False, max_length=32)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('full_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=20)),
                ('street_address1', models.CharField(max_length=80)),
                ('street_address2', models.CharField(blank=True, max_length=80, null=True)),
                ('postcode', models.CharField(blank=True, max_length=20, null=True)),
                ('town_or_city', models.CharField(max_length=40)),
                ('county', models.CharField(blank=True, max_length=80, null=True)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('SUCCESS', 'Success'), ('FAILED', 'Failed'), ('PENDING', 'Pending')], default='PENDING', max_length=20)),
                ('grand_total', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('stripe_payment_intent_id', models.CharField(blank=True, max_length=254, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectFunding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donations.payment')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='os_project.project')),
            ],
        ),
        migrations.CreateModel(
            name='WITFunding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donations.payment')),
                ('wit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_profile.womenintech')),
            ],
        ),
    ]
