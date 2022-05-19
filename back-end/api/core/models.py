import random
from django.db import models

from .getTechs import getTechs

# Create your models here.


class CVE(models.Model):
    description = models.TextField(blank=True)

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


class Subdomain(models.Model):
    name = models.CharField(max_length=50)
    include = models.BooleanField(default=True)
    techs = models.ManyToManyField(Tech)

    """ def save(self, *args, **kwargs):
        response = getTechs(self.name)
        techs_to_add = []
        try:
            response = response[0]["technologies"]
        except:
            print("No Technologies Found!")

        for tech in response:
            randColor = "%06x" % random.randint(0, 0xFFFFFF)
            techs_to_add.append(
                {
                    "name": tech["name"],
                    "versions": {"arr": tech["versions"]},
                    "cves": [],
                    "color": randColor,
                }
            )
        self.techs.set(techs_to_add)
        print(self)
        super(models.Model, self).save(*args, **kwargs) """

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
