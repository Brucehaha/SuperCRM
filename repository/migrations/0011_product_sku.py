# Generated by Django 2.1.5 on 2019-05-25 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0010_remove_product_sku'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sku',
            field=models.CharField(blank=True, max_length=16, null=True, unique=True),
        ),
    ]