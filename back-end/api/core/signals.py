from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver

from .tasks import async_get_domain_data
from .utilities import getCVEs
from django_celery_beat.models import PeriodicTask
from .periodic import periodic_update_domain_CVEs


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


@receiver(pre_save, sender=Domain)
def changeCronJob(sender, instance, **kwargs):
    try:
        oldDomain = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass  # Object is new, so field hasn't technically changed, but you may want to do something else here.
    else:
        if not oldDomain.cron_interval == instance.cron_interval:  # Field has changed
            print("Changing Cron Job")
            taskQuery = f"Updating {str(instance.id)} : {instance.name}  CVEs"
            periodicTasks = PeriodicTask.objects.filter(name=taskQuery)
            for task in periodicTasks:
                task.delete()
            periodic_update_domain_CVEs(instance.id, instance.cron_interval)

        else:  # field has not changed
            print("No Need To Change Cron job")

        if not oldDomain.verified == instance.verified:
            if instance.verified:
                async_get_domain_data.delay(instance.id)
