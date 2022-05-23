from django.db import models

from .utilities import getCVEs, vulnerability

# Create your models here.


class CVE(models.Model):
    def json_default():
        return {"arr": []}

    description = models.TextField(blank=True)
    severity = models.CharField(max_length=20)
    score = models.CharField(max_length=5)
    references = models.JSONField(default=json_default)

    def __str__(self):
        return self.description


class Tech(models.Model):
    def json_default():
        return {"arr": []}

    name = models.CharField(max_length=100)
    versions = models.JSONField(default=json_default)
    cves = models.ManyToManyField(CVE, blank=True)
    color = models.CharField(max_length=6, default="828192")

    def __str__(self):
        return "%s" % (self.name)

    def save(self, *args, **kwargs):
        print("save override")
        versions = self.versions["arr"]
        version = ""
        if not versions:
            version = ""
        else:
            version = versions[0]

        print(version)
        response = getCVEs(self.name)
        print(response)
        super(Tech, self).save(*args, **kwargs)


class Subdomain(models.Model):
    name = models.CharField(max_length=50)
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
    photo = models.CharField(blank=True, max_length=350)

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
