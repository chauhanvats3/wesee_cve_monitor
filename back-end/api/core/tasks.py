from ensurepip import version
import random
import this
import time
from celery import shared_task
from .utilities import getPhoto, getTechs, getCVEs, findSubdomains
from django.apps import apps
from .periodic import update_domain_two_hours


@shared_task
def async_save_subdomains(domainId, subdomainName):
    print("async save subdomains : " + subdomainName)
    domainModel = apps.get_model(app_label="core", model_name="Domain")
    thisDomain = domainModel.objects.get(pk=domainId)
    thisDomain.subdomains.create(name=subdomainName, include=True)
    print("subdomain created : " + subdomainName)


@shared_task
def async_save_domain_tech(domainId, techName, localversions):
    print("Save Domain Tech : " + techName)
    domainModel = apps.get_model(app_label="core", model_name="Domain")
    thisDomain = domainModel.objects.get(pk=domainId)
    randColor = "%06x" % random.randint(0, 0xFFFFFF)
    arr = {"arr": localversions}
    thisDomain.techs.create(name=techName, versions=arr, color=randColor)
    print("Domain Tech Created : " + techName)


@shared_task
def async_save_subdomain_techs(subdomainId, techName, localVersions):
    print("Save Subdomain Tech : " + techName)
    subdomainModel = apps.get_model(app_label="core", model_name="Subdomain")
    thisSubdomain = subdomainModel.objects.get(pk=subdomainId)
    randColor = "%06x" % random.randint(0, 0xFFFFFF)
    arr = {"arr": localVersions}
    thisSubdomain.techs.create(name=techName, versions=arr, color=randColor)
    print("Saved Subdomain Techs : " + thisSubdomain.name)


def saveSubdomains(thisDomain):
    subdomainsResponse = findSubdomains(thisDomain.name)
    try:
        for subdomain in subdomainsResponse["FDNS_A"]:
            subdomainName = subdomain.split(",")[1]
            time.sleep(3)
            async_save_subdomains.delay(thisDomain.id, subdomainName)
            print("Subdomains saved for : " + thisDomain.name)
    except:
        print("Subdomains Not Found")


def saveTechs(thisDomain):
    techResponse = getTechs(thisDomain.full_name)
    try:
        for tech in techResponse[0]["technologies"]:
            techName = tech["name"]
            versions = tech["versions"]
            time.sleep(3)
            async_save_domain_tech.delay(thisDomain.id, techName, versions)
            print("Saved Domain Techs : " + thisDomain.name)

    except:
        print("Some Error Occurred in getting Tech")


@shared_task
def async_get_domain_data(domainId):
    domainModel = apps.get_model(app_label="core", model_name="Domain")
    thisDomain = domainModel.objects.get(pk=domainId)
    if thisDomain.saved_already == False:
        print("Getting Subdomains : " + thisDomain.name)
        saveSubdomains(thisDomain)

        print("Getting Domain Techs : " + thisDomain.name)
        saveTechs(thisDomain)

        thisDomain.saved_already = True
        thisDomain.save(update_fields=["saved_already"])

        update_domain_two_hours(domainId)

        print("Data Set Async completed")
    print("Data Already Set")


@shared_task
def async_get_subdomain_techs(subdomainId):
    SubdomainModel = apps.get_model(app_label="core", model_name="Subdomain")
    thisSubdomain = SubdomainModel.objects.get(pk=subdomainId)
    for oldTech in thisSubdomain.techs.all():
        oldTech.delete()
    print("Getting Subdomain Techs : " + thisSubdomain.name)
    techResponse = getTechs(thisSubdomain.name)
    try:
        for tech in techResponse[0]["technologies"]:
            techName = tech["name"]
            versions = tech["versions"]
            time.sleep(3)
            async_save_subdomain_techs.delay(subdomainId, techName, versions)

    except:
        print("Some Error Occurred in getting Tech")


@shared_task
def async_get_tech_cve(techId):
    print(techId)
    TechModel = apps.get_model(app_label="core", model_name="Tech")
    thisTech = TechModel.objects.get(pk=techId)
    thisTech.save()


@shared_task
def async_update_domain_cve(*args):
    domainId = args[0]
    domainModel = apps.get_model(app_label="core", model_name="Domain")
    thisDomain = domainModel.objects.get(pk=domainId)
    print("Updating CVEs for : " + thisDomain.name)
    for tech in thisDomain.techs.all():
        async_get_tech_cve.delay(tech.id)
    for subdomain in thisDomain.subdomains.all():
        for tech in subdomain.tehs.all():
            async_get_tech_cve.delay(tech.id)
