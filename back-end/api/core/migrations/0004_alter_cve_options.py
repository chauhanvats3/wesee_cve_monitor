# Generated by Django 4.0.4 on 2022-06-08 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_cve_cve_id_cve_isnew'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cve',
            options={'ordering': ('-isNew',)},
        ),
    ]
