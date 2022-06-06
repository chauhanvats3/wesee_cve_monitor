from pickle import TRUE
import random
from urllib import request
from django.db import models
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.backends import TokenBackend
from .utilities import getPhoto, getTechs, getCVEs, findSubdomains
from .tasks import async_get_domain_data, async_get_subdomain_techs


from .utilities import getCVEs


class CVE(models.Model):
    def json_default():
        return {"arr": []}

    description = models.TextField(blank=True)
    severity = models.CharField(max_length=20)
    score = models.CharField(max_length=5)
    references = models.JSONField(default=json_default)
    tech_id = models.CharField(max_length=5)

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        super(CVE, self).save(*args, **kwargs)
        self.techno.add(self.tech_id)


class Tech(models.Model):
    def json_default():
        return {"arr": []}

    name = models.CharField(max_length=100)
    versions = models.JSONField(default=json_default)
    cves = models.ManyToManyField(CVE, blank=True, related_name="techno")
    color = models.CharField(max_length=6, default="828192")

    def __str__(self):
        return "%s " % (self.name)

    def save(self, *args, **kwargs):
        super(Tech, self).save(*args, **kwargs)
        for old_cve in self.cves.all():
            old_cve.delete()
        versions = self.versions["arr"]
        version = ""
        if not versions:
            version = ""
        else:
            version = versions[0]

        response = getCVEs(self.name, version)
        for eachCVE in response:
            arr = {"arr": eachCVE["references"]}
            cve = None
            cve = self.cves.create(
                description=eachCVE["description"],
                severity=eachCVE["severity"],
                score=eachCVE["score"],
                references=arr,
                tech_id=self.id,
            )
            self.cves.add(cve)


class Subdomain(models.Model):
    name = models.CharField(max_length=50)
    include = models.BooleanField(default=True)
    techs = models.ManyToManyField(Tech)
    techs_fetched = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % (self.name)

    def save(self, *args, **kwargs):
        super(Subdomain, self).save(*args, **kwargs)
        async_get_subdomain_techs.delay(self.id)

        """ for old_techs in self.techs.all():
            old_techs.delete()

        try:
            response = getTechs(self.name)
            for tech in response[0]["technologies"]:
                randColor = "%06x" % random.randint(0, 0xFFFFFF)
                arr = {"arr": tech["versions"]}
                tech = self.techs.create(
                    name=tech["name"], versions=arr, color=randColor
                )
                self.techs.add(tech)
        except:
            print("No techs Found") 

        self.techs_fetched = True"""


class Domain(models.Model):
    full_name = models.URLField(unique=True)
    verified = models.BooleanField(default=False)
    enumerate = models.BooleanField(default=False)
    subdomains = models.ManyToManyField(Subdomain, blank=True)
    techs = models.ManyToManyField(Tech, blank=True)
    verify_code = models.PositiveIntegerField()
    photo = models.CharField(max_length=550, blank=True)
    author = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    saved_already = models.BooleanField(default=False)

    @property
    def name(self):
        return self.full_name.split("://")[1]

    @property
    def protocol(self):
        return self.full_name.split("://")[0]

    def __str__(self):
        return "%s : %s" % (self.name, self.protocol)

    def save(self, *args, **kwargs):
        if self._state.adding == True:
            # get PHOTO on Create Only
            photoUrl = getPhoto()
            self.photo = photoUrl
            print("Photo Added : " + photoUrl)
        super(Domain, self).save(*args, **kwargs)
        async_get_domain_data.delay(self.id)
