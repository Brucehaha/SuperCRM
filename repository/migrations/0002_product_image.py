# Generated by Django 2.1.5 on 2019-06-28 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ManyToManyField(blank=True, null=True, to='repository.Image'),
        ),
    ]
