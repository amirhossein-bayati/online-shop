# Generated by Django 3.2.8 on 2021-10-16 07:28

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_product_status'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='product',
            managers=[
                ('published', django.db.models.manager.Manager()),
            ],
        ),
    ]
