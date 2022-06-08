from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from .utilities import getCVEs
from django_celery_beat.models import PeriodicTask


from .models import Domain, Subdomain, Tech, CVE


@receiver(pre_delete, sender=Domain)
def cascadeDeleteDomain(sender, instance, **kwargs):
    for subdomain in instance.subdomains.all():
        subdomain.delete()
    for tech in instance.techs.all():
        tech.delete()
    taskQuery = "Updating " + str(instance.id) + " CVEs"
    periodicTasks = PeriodicTask.objects.filter(name=taskQuery)
    for task in periodicTasks:
        task.delete()


@receiver(pre_delete, sender=Subdomain)
def cascadeDeleteSubdomain(sender, instance, **kwargs):
    for tech in instance.techs.all():
        tech.delete()


@receiver(pre_delete, sender=Tech)
def cascadeDeleteTech(sender, instance, **kwargs):
    for cve in instance.cves.all():
        cve.delete()


""" @receiver(pre_save, sender=Tech)
def do_something_if_changed(sender, instance, **kwargs):
    try:
        oldTech = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass  # Object is new, so field hasn't technically changed, but you may want to do something else here.
    else:
        if not oldTech.versions == instance.versions:  # Field has changed
            for old_cve in instance.cves.all():
                old_cve.delete()
        else:  # field has not changed
            print(oldTech.id)
 """
