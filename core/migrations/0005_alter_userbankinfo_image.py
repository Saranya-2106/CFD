# Generated by Django 4.1.2 on 2022-12-21 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_userbankinfo_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbankinfo',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pic/'),
        ),
    ]
