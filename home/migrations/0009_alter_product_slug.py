# Generated by Django 5.1.1 on 2024-09-15 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_order_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(auto_created=models.CharField(max_length=500)),
        ),
    ]
