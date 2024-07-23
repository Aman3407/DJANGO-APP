# Generated by Django 5.0.7 on 2024-07-23 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_rename_supplier_item_suppliers'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='item_id',
            field=models.IntegerField(default=1, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='supplier',
            name='contact',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='email',
            field=models.EmailField(blank=True, max_length=254, unique=True),
        ),
    ]
