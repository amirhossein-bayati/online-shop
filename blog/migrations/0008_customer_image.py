# Generated by Django 3.2.8 on 2021-10-23 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20211022_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]