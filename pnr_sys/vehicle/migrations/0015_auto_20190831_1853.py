# Generated by Django 2.2.4 on 2019-08-31 10:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0014_log_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='first_entry_at',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='registered_at',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
    ]
