# Generated by Django 3.2.6 on 2021-09-01 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loader', '0002_hubloader_user'),
        ('hubmanager', '0003_logichub_loaders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logichub',
            name='loaders',
            field=models.ManyToManyField(blank=True, related_name='loader_list', to='loader.HubLoader'),
        ),
    ]
