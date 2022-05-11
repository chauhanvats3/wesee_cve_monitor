# Generated by Django 4.0.4 on 2022-05-09 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_domain_subdomains_domain_subdomains_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='domain',
            name='subdomains',
        ),
        migrations.AddField(
            model_name='domain',
            name='subdomains',
            field=models.ManyToManyField(to='core.subdomain'),
        ),
        migrations.RemoveField(
            model_name='domain',
            name='techs',
        ),
        migrations.AddField(
            model_name='domain',
            name='techs',
            field=models.ManyToManyField(to='core.tech'),
        ),
        migrations.RemoveField(
            model_name='subdomain',
            name='techs',
        ),
        migrations.AddField(
            model_name='subdomain',
            name='techs',
            field=models.ManyToManyField(to='core.tech'),
        ),
        migrations.RemoveField(
            model_name='tech',
            name='cves',
        ),
        migrations.AddField(
            model_name='tech',
            name='cves',
            field=models.ManyToManyField(to='core.cve'),
        ),
        migrations.RemoveField(
            model_name='user',
            name='domains',
        ),
        migrations.AddField(
            model_name='user',
            name='domains',
            field=models.ManyToManyField(to='core.domain'),
        ),
    ]
