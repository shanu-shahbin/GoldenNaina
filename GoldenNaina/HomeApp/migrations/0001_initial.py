# Generated by Django 4.2.14 on 2024-08-04 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TermsAndConditions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('period', models.CharField(max_length=255)),
                ('offer_details', models.TextField()),
                ('conditions', models.TextField()),
            ],
        ),
    ]
