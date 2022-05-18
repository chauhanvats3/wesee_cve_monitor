from enum import unique
from django.db import models

# Create your models here.


class CVE(models.Model):
    description = models.TextField(blank=True)

    def __str__(self):
        return self.description


class Tech(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    cves = models.ManyToManyField(CVE)
    color = models.CharField(max_length=6, default="828192")

    class Meta:
        unique_together = ["name", "version"]

    def __str__(self):
        return "%s [%s]" % (self.name, self.version)


class Subdomain(models.Model):
    name = models.CharField(max_length=50, unique=True)
    include = models.BooleanField(default=True)
    techs = models.ManyToManyField(Tech)

    def __str__(self):
        return "%s" % (self.name)


class Domain(models.Model):
    full_name = models.URLField(unique=True)
    verified = models.BooleanField(default=False)
    enumerate = models.BooleanField(default=False)
    subdomains = models.ManyToManyField(Subdomain, blank=True)
    techs = models.ManyToManyField(Tech, blank=True)
    verify_code = models.PositiveIntegerField()

    @property
    def name(self):
        return self.full_name.split("://")[1]

    @property
    def protocol(self):
        return self.full_name.split("://")[0]

    def __str__(self):
        return "%s : %s" % (self.name, self.protocol)


class User(models.Model):
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=32)
    domains = models.ManyToManyField(Domain)

    def __str__(self):
        return "%s" % (self.email)
