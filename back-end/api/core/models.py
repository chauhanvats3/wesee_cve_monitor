from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.backends import TokenBackend
from .utilities import getPhoto
from .tasks import async_get_domain_data, async_get_subdomain_techs, async_get_tech_cves


from .utilities import getCVEs


class CVE(models.Model):
    def json_default():
        return {"arr": []}

    description = models.TextField(blank=True)
    severity = models.CharField(max_length=20)
    score = models.CharField(max_length=5)
    references = models.JSONField(default=json_default)
    tech_id = models.CharField(max_length=5)
    cve_id = models.CharField(max_length=50, default="")
    isNew = models.BooleanField(default=True)
    isSeen = models.BooleanField(default=False)

    def __str__(self):
        return self.cve_id

    def save(self, *args, **kwargs):
        super(CVE, self).save(*args, **kwargs)
        self.techno.add(self.tech_id)

    class Meta:
        ordering = ("-isNew",)


class Tech(models.Model):
    def json_default():
        return {"arr": []}

    name = models.CharField(max_length=100)
    versions = models.JSONField(default=json_default)
    cves = models.ManyToManyField(CVE, blank=True, related_name="techno")
    color = models.CharField(max_length=6, default="828192")
    updating_cve = models.BooleanField(default=True)

    def __str__(self):
        return "%s " % (self.name)

    def save(self, *args, **kwargs):
        super(Tech, self).save(*args, **kwargs)
        async_get_tech_cves.delay(self.id)


class Subdomain(models.Model):
    name = models.CharField(max_length=50)
    include = models.BooleanField(default=True)
    techs = models.ManyToManyField(Tech)
    techs_fetched = models.BooleanField(default=False)
    created_date = models.DateTimeField("date created", default=timezone.now)

    def __str__(self):
        return "%s" % (self.name)

    def save(self, *args, **kwargs):
        super(Subdomain, self).save(*args, **kwargs)
        async_get_subdomain_techs.delay(self.id)

    class Meta:
        ordering = ["-created_date"]


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
    cron_interval = models.PositiveSmallIntegerField(default=2)

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
