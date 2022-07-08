from enum import unique
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from celery import group
from .utilities import getPhoto
from .tasks import async_get_subdomain_techs, async_get_tech_cves


class CVE(models.Model):
    def json_default():
        return {"arr": []}

    description = models.TextField(blank=True, editable=False)
    severity = models.CharField(max_length=20, editable=False)
    score = models.CharField(max_length=5, editable=False)
    references = models.JSONField(default=json_default)
    tech_id = models.CharField(max_length=10)
    cve_id = models.CharField(max_length=50, default="", editable=False)
    isNew = models.BooleanField(default=True)
    isSeen = models.BooleanField(default=False)

    def __str__(self):
        tech = list(self.techno.all())[0]
        if tech.subdomain_set.count() != 0:
            subdomain = list(tech.subdomain_set.all())[0]
            domain = list(subdomain.domain_set.all())[0]
            return f"{domain.name} : {subdomain.name} : {tech.name} : {self.cve_id}"

        elif tech.domain_set.count() != 0:
            domain = list(tech.domain_set.all())[0]
            return f"{domain.name} : {tech.name} : {self.cve_id}"
        else:
            return f"{self.cve_id}"

    def save(self, *args, **kwargs):
        super(CVE, self).save(*args, **kwargs)
        self.techno.add(self.tech_id)

    class Meta:
        ordering = ("-isNew",)
        unique_together = (
            "cve_id",
            "tech_id",
        )


class Tech(models.Model):
    def json_default():
        return {"arr": []}

    name = models.CharField(max_length=100, editable=False)
    versions = models.JSONField(default=json_default)
    cves = models.ManyToManyField(CVE, blank=True, related_name="techno")
    color = models.CharField(max_length=6, default="828192", editable=False)
    updating_cve = models.BooleanField(default=True)
    author = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.CASCADE, editable=False
    )

    def __str__(self):
        if self.domain_set.count() != 0:
            domain = list(self.domain_set.all())[0]
            return f"{domain.name} :  {self.name}"

        elif self.subdomain_set.count() != 0:
            subdomain = list(self.subdomain_set.all())[0]
            domain = list(subdomain.domain_set.all())[0]
            return f"{domain.name} : {subdomain.name} : {self.name}"
        else:
            return f"{self.name}"

    def save(self, *args, **kwargs):
        super(Tech, self).save(*args, **kwargs)
        async_get_tech_cves.delay(self.id, False)


class Subdomain(models.Model):
    name = models.CharField(max_length=50, editable=False)
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
    full_name = models.URLField(unique=True, editable=False)
    verified = models.BooleanField(default=False)
    enumerate = models.BooleanField(default=False)
    subdomains = models.ManyToManyField(Subdomain, blank=True)
    techs = models.ManyToManyField(Tech, blank=True)
    verify_code = models.PositiveIntegerField(editable=False)
    photo = models.CharField(max_length=550, blank=True, editable=False)
    author = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.CASCADE, editable=False
    )
    saved_already = models.BooleanField(default=False)
    cron_interval = models.PositiveSmallIntegerField(default=2)
    fetching_subdomains = models.BooleanField(default=True)

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
