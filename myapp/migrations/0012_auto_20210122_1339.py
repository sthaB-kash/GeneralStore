# Generated by Django 3.1.3 on 2021-01-22 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_notification_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='date_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
