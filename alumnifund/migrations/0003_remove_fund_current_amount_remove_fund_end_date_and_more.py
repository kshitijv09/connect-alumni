# Generated by Django 5.1.6 on 2025-04-05 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnifund', '0002_fund_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fund',
            name='current_amount',
        ),
        migrations.RemoveField(
            model_name='fund',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='fund',
            name='target_amount',
        ),
    ]
