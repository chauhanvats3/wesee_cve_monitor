from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from .utilities import getCVEs


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


@receiver(pre_save, sender=Tech)
def addCVEs(sender, instance, **kwargs):
    print(instance, instance.versions)
