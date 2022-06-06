from ensurepip import version
import random
from celery import shared_task
from .utilities import getPhoto, getTechs, getCVEs, findSubdomains
from django.apps import apps


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
def async_get_domain_data(domainId):
    domainModel = apps.get_model(app_label="core", model_name="Domain")
    thisDomain = domainModel.objects.get(pk=domainId)
    if thisDomain.saved_already == False:
        print("Getting Subdomains : " + thisDomain.name)
        subdomainsResponse = findSubdomains(thisDomain.name)
        try:
            for subdomain in subdomainsResponse["FDNS_A"]:
                subdomainName = subdomain.split(",")[1]
                async_save_subdomains.delay(domainId, subdomainName)
                print("Subdomains saved for : " + thisDomain.name)
        except:
            print("Subdomains Not Found")

        print("Getting Domain Techs : " + thisDomain.name)
        techResponse = getTechs(thisDomain.full_name)
        try:
            for tech in techResponse[0]["technologies"]:
                techName = tech["name"]
                versions = tech["versions"]
                async_save_domain_tech.delay(domainId, techName, versions)
                print("Saved Domain Techs : " + thisDomain.name)

        except:
            print("Some Error Occurred in getting Tech")

        thisDomain.saved_already = True
        thisDomain.save(update_fields=["saved_already"])
        print("Data Set Async completed")
    print("Data Already Set")
