# Generated by Django 4.2.3 on 2023-08-05 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_product_sex'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categories',
            name='description',
        ),
        migrations.AddField(
            model_name='categories',
            name='parent_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='core.categories'),
        ),
    ]