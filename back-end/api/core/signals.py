from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver

from .getTechs import getTechs

from .models import Domain, Subdomain, Tech, CVE


@receiver(pre_delete, sender=Domain)
def cascadeDeleteDomain(sender, instance, **kwargs):
    for subdomain in instance.subdomains.all():
        subdomain.delete()
    for tech in instance.techs.all():
        tech.delete()


@receiver(pre_delete, sender=Subdomain)
def cascadeDeleteSubdomain(sender, instance, **kwargs):
    for tech in instance.techs.all():
        tech.delete()


@receiver(pre_delete, sender=Tech)
def cascadeDeleteTech(sender, instance, **kwargs):
    for cve in instance.cves.all():
        cve.delete()


@receiver(post_save, sender=Domain)
def addSubdomainTEch(sender, instance, **kwargs):
    for subdomain in instance.subdomains.all():
        print(subdomain)
