# Generated by Django 4.2.3 on 2023-08-16 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_subscribe'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscribe',
            name='used',
            field=models.BooleanField(default=bool),
            preserve_default=False,
        ),
    ]