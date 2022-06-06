from ensurepip import version
import random
from celery import shared_task
from .utilities import getPhoto, getTechs, getCVEs, findSubdomains
from django.apps import apps


@shared_task
def async_save_subdomains(domainId, subdomainName):
    print("Saving Subdomains")
    domainModel = apps.get_model(app_label="core", model_name="Domain")
    thisDomain = domainModel.objects.get(pk=domainId)
    thisDomain.subdomains.create(name=subdomainName, include=True)


@shared_task
def async_save_domain_tech(domainId, name, localversions):
    print("Saving Domain Tech")
    domainModel = apps.get_model(app_label="core", model_name="Domain")
    thisDomain = domainModel.objects.get(pk=domainId)
    randColor = "%06x" % random.randint(0, 0xFFFFFF)
    arr = {"arr": localversions}
    thisDomain.techs.create(name, versions=arr, color=randColor)


@shared_task
def async_get_domain_data(domainId):
    domainModel = apps.get_model(app_label="core", model_name="Domain")
    thisDomain = domainModel.objects.get(pk=domainId)
    if thisDomain.saved_already == False:
        print("Getting Subdomains")
        subdomainsResponse = findSubdomains(thisDomain.name)
        print(subdomainsResponse)
        try:
            for subdomain in subdomainsResponse["FDNS_A"]:
                subdomainName = subdomain.split(",")[1]
                async_save_subdomains.delay(domainId, subdomainName)
                # thisDomain.subdomains.add(subdomain)
        except:
            print("Subdomains Not Found")

        print("Getting Domain Techs")
        techResponse = getTechs(thisDomain.full_name)
        try:
            for tech in techResponse[0]["technologies"]:
                techName = tech["name"]
                versions = tech["versions"]
                async_save_domain_tech.delay(domainId, techName, versions)
        except:
            print("Some Error Occurred in getting Tech")

        thisDomain.saved_already = True
        thisDomain.save(update_fields=["saved_already"])
        print("Data Set Async")
    print("Data Already Set")


@shared_task
def async_get_cve(tech_id):
    print("Getting CVE")
    techModel = apps.get_model(app_label="core", model_name="Tech")
    thisTech = techModel.objects.get(pk=tech_id)
    for old_cve in thisTech.cves.all():
        old_cve.delete()
    print("Deleted old")
    versions = thisTech.versions["arr"]
    version = ""
    if not versions:
        version = ""
    else:
        version = versions[0]
    response = getCVEs(thisTech.name, version)
    print("got response from server")
    try:
        for eachCVE in response:
            arr = {"arr": eachCVE["references"]}
            cve = None
            cve = thisTech.cves.create(
                description=eachCVE["description"],
                severity=eachCVE["severity"],
                score=eachCVE["score"],
                references=arr,
                tech_id=thisTech.id,
            )
            thisTech.cves.add(cve)
    except:
        print("Error in Getting CVE for : " + thisTech.name)
