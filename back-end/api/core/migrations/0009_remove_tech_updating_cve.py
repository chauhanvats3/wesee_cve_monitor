# Generated by Django 4.0.4 on 2022-06-10 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_subdomain_options_tech_updating_cve'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tech',
            name='updating_cve',
        ),
    ]
