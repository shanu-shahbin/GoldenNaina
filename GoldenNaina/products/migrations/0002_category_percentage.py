# Generated by Django 4.2.14 on 2024-08-07 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='percentage',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
