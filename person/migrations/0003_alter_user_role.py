# Generated by Django 5.1.6 on 2025-03-30 07:12

import django.db.models.deletion
import person.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0002_alter_user_bio_alter_user_linkedin_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.ForeignKey(default=person.models.get_default_user_role, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='person.userrole'),
        ),
    ]
