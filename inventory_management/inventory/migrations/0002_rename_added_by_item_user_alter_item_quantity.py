# Generated by Django 5.0.7 on 2024-07-19 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='added_by',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='item',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]
