# Generated by Django 5.0.4 on 2025-07-22 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Service_app', '0002_alter_service_duration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='location',
            new_name='Type',
        ),
        migrations.AddField(
            model_name='vehicle',
            name='km_run',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='last_service_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
