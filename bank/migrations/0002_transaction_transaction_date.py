# Generated by Django 5.1.5 on 2025-01-26 02:38

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='transaction_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
