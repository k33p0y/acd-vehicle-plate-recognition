# Generated by Django 2.2.4 on 2019-08-29 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0012_auto_20190829_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
