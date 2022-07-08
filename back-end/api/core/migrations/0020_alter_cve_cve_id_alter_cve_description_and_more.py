# Generated by Django 4.0.4 on 2022-07-08 15:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0019_domain_fetching_subdomains'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cve',
            name='cve_id',
            field=models.CharField(default='', editable=False, max_length=50),
        ),
        migrations.AlterField(
            model_name='cve',
            name='description',
            field=models.TextField(blank=True, editable=False),
        ),
        migrations.AlterField(
            model_name='cve',
            name='score',
            field=models.CharField(editable=False, max_length=5),
        ),
        migrations.AlterField(
            model_name='cve',
            name='severity',
            field=models.CharField(editable=False, max_length=20),
        ),
        migrations.AlterField(
            model_name='domain',
            name='author',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='domain',
            name='full_name',
            field=models.URLField(editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='domain',
            name='photo',
            field=models.CharField(blank=True, editable=False, max_length=550),
        ),
        migrations.AlterField(
            model_name='domain',
            name='verify_code',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='subdomain',
            name='name',
            field=models.CharField(editable=False, max_length=50),
        ),
        migrations.AlterField(
            model_name='tech',
            name='author',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tech',
            name='color',
            field=models.CharField(default='828192', editable=False, max_length=6),
        ),
        migrations.AlterField(
            model_name='tech',
            name='name',
            field=models.CharField(editable=False, max_length=100),
        ),
    ]