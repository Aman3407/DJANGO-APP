# Generated by Django 5.0.7 on 2024-07-28 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_alter_supplier_contact_alter_supplier_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='quantityInStock',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='item',
            name='quantitySold',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
