# Generated by Django 4.0.4 on 2022-06-08 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cve',
            name='cve_id',
        ),
        migrations.RemoveField(
            model_name='cve',
            name='isNew',
        ),
    ]