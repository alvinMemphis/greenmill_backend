# Generated by Django 3.2.6 on 2021-08-27 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0003_alter_package_supplier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]