# Generated by Django 4.0.4 on 2022-07-07 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_alter_domain_author_alter_domain_verify_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='domain',
            name='fetching_subdomains',
            field=models.BooleanField(default=True),
        ),
    ]
