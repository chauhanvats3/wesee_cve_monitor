from urllib import request
from django.db import models
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.backends import TokenBackend


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
    author = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)

    @property
    def name(self):
        return self.full_name.split("://")[1]

    @property
    def protocol(self):
        return self.full_name.split("://")[0]

    def __str__(self):
        return "%s : %s" % (self.name, self.protocol)


"""     def save(self, *args, **kwargs):
        super(Domain, self).save(*args, **kwargs)
        token = request.META.get("HTTP_AUTHORIZATION", " ").split(" ")[1]
        data = {"token": token}
        try:
            valid_data = TokenBackend(algorithm="HS256").decode(token, verify=True)
            user = valid_data["user"]
        except:
            print("validation error")
        self.author = user """
