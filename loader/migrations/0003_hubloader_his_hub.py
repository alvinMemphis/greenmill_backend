# Generated by Django 3.2.6 on 2021-09-01 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hubmanager', '0005_remove_logichub_loaders'),
        ('loader', '0002_hubloader_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='hubloader',
            name='his_hub',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='hubs', to='hubmanager.logichub'),
        ),
    ]
