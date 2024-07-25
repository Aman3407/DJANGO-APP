# Generated by Django 5.0.7 on 2024-07-24 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('contact', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=100)),
                ('quantityInStock', models.PositiveIntegerField()),
                ('quantitySold', models.PositiveIntegerField()),
                ('revenue', models.DecimalField(decimal_places=2, max_digits=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('suppliers', models.ManyToManyField(to='inventory.supplier')),
            ],
        ),
    ]
