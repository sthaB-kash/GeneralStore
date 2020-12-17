# Generated by Django 3.1.3 on 2020-11-22 04:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_supplier'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supplier',
            name='product',
        ),
        migrations.AddField(
            model_name='product',
            name='supplier',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.supplier'),
            preserve_default=False,
        ),
    ]
