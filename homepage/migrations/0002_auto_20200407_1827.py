# Generated by Django 3.0.3 on 2020-04-07 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.CharField(default='', max_length=10000),
        ),
    ]