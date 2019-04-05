# Generated by Django 2.1.5 on 2019-04-05 03:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='icons',
            field=models.CharField(default=django.utils.timezone.now, max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='menu',
            name='url_name',
            field=models.CharField(max_length=128),
        ),
    ]