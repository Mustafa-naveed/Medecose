# Generated by Django 5.1.1 on 2024-09-14 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_slider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slider',
            name='sliderImage',
            field=models.ImageField(upload_to='Media'),
        ),
    ]
