# Generated by Django 2.2.28 on 2025-03-19 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='editednotes',
            name='EditedID',
        ),
        migrations.AddField(
            model_name='editednotes',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
