import random
import time
from celery import shared_task
from .utilities import getPhoto, getTechs, getCVEs, findSubdomains
from django.apps import apps
from .periodic import periodic_update_domain_CVEs


@shared_task
def async_create_subdomains(domainId, subdomainName):
    print("async save subdomains : " + subdomainName)
    domainModel = apps.get_model(app_label="core", model_name="Domain")
    thisDomain = domainModel.objects.get(pk=domainId)
    thisDomain.subdomains.create(name=subdomainName, include=True)
    print("subdomain created : " + subdomainName)


@shared_task
def async_create_domain_tech(domainId, techName, localversions):
    print("Save Domain Tech : " + techName)
    domainModel = apps.get_model(app_label="core", model_name="Domain")
    thisDomain = domainModel.objects.get(pk=domainId)
    randColor = "%06x" % random.randint(0, 0xFFFFFF)
    arr = {"arr": localversions}
    thisDomain.techs.create(
        name=techName, versions=arr, color=randColor, updating_cve=True
    )
    print("Domain Tech Created : " + techName)


@shared_task
def async_create_subdomain_techs(subdomainId, techName, localVersions):
    print("Save Subdomain Tech : " + techName)
    subdomainModel = apps.get_model(app_label="core", model_name="Subdomain")
    thisSubdomain = subdomainModel.objects.get(pk=subdomainId)
    randColor = "%06x" % random.randint(0, 0xFFFFFF)
    arr = {"arr": localVersions}
    thisSubdomain.techs.create(
        name=techName, versions=arr, color=randColor, updating_cve=True
    )
    print("Saved Subdomain Techs : " + thisSubdomain.name)


def saveSubdomains(thisDomain):
    subdomainsResponse = findSubdomains(thisDomain.name)
    try:
        for subdomain in subdomainsResponse["FDNS_A"]:
            subdomainName = subdomain.split(",")[1]
            time.sleep(3)
            async_create_subdomains.delay(thisDomain.id, subdomainName)
            print("Subdomains saved for : " + thisDomain.name)
    except:
        print("Subdomains Not Found")


def saveTechs(thisDomain):
    techResponse = getTechs(thisDomain.full_name)
    print(techResponse)
    try:
        for tech in techResponse[0]["technologies"]:
            techName = tech["name"]
            versions = tech["versions"]
            time.sleep(3)
            async_create_domain_tech.delay(thisDomain.id, techName, versions)
            print("Saved Domain Techs : " + thisDomain.name)

    except:
        print("Some Error Occurred in getting Tech")


@shared_task
def async_get_domain_data(domainId):
    domainModel = apps.get_model(app_label="core", model_name="Domain")
    thisDomain = domainModel.objects.get(pk=domainId)
    if thisDomain.saved_already == False:

        thisDomain.saved_already = True
        thisDomain.save(update_fields=["saved_already"])

        print("async_getDomain_data")
        print("Getting Domain Techs : " + thisDomain.name)
        saveTechs(thisDomain)

        print("Getting Subdomains : " + thisDomain.name)
        saveSubdomains(thisDomain)

        periodic_update_domain_CVEs(domainId, thisDomain.cron_interval)

        print("Data Set Async completed")
    else:
        print("Domain Data Already Set")


@shared_task
def async_get_subdomain_techs(subdomainId):
    SubdomainModel = apps.get_model(app_label="core", model_name="Subdomain")
    thisSubdomain = SubdomainModel.objects.get(pk=subdomainId)
    if thisSubdomain.techs_fetched == False:
        for oldTech in thisSubdomain.techs.all():
            oldTech.delete()
        print("Getting Subdomain Techs : " + thisSubdomain.name)
        techResponse = getTechs(thisSubdomain.name)
        try:
            for tech in techResponse[0]["technologies"]:
                techName = tech["name"]
                versions = tech["versions"]
                time.sleep(3)
                async_create_subdomain_techs.delay(subdomainId, techName, versions)

        except:
            print("Some Error Occurred in getting Tech")

        finally:
            thisSubdomain.techs_fetched = True
            thisSubdomain.save()
    else:
        print("Techs already fetched")


@shared_task
def async_refresh_tech_cve(techId):
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
        async_refresh_tech_cve.delay(tech.id)
    for subdomain in thisDomain.subdomains.all():
        for tech in subdomain.tehs.all():
            async_refresh_tech_cve.delay(tech.id)


@shared_task
def async_get_tech_cves(techId):
    techModel = apps.get_model(app_label="core", model_name="Tech")
    thisTech = techModel.objects.get(pk=techId)
    oldCVEs = []
    if thisTech.updating_cve is True:
        for old_cve in thisTech.cves.all():
            oldCVEs.append({"cve_id": old_cve.cve_id, "isSeen": old_cve.isSeen})
            old_cve.delete()

        versions = thisTech.versions["arr"]
        version = ""
        if not versions:
            version = ""
        else:
            version = versions[0]

        response = getCVEs(thisTech.name, version)

        for eachCVE in response:
            isThisNew = True
            for old in oldCVEs:
                if old["cve_id"] == eachCVE["cve_id"] and old["isSeen"] == True:
                    isThisNew = False
            arr = {"arr": eachCVE["references"]}
            cve = None
            cve = thisTech.cves.create(
                description=eachCVE["description"],
                severity=eachCVE["severity"],
                score=eachCVE["score"],
                cve_id=eachCVE["cve_id"],
                references=arr,
                isNew=isThisNew,
                tech_id=thisTech.id,
            )
            thisTech.cves.add(cve)
        thisTech.updating_cve = False
        thisTech.save()
    else:
        print("Not Updating CVEs")


@shared_task
def async_mark_cve_seen(techId):
    print("Marking...")
    techModel = apps.get_model(app_label="core", model_name="Tech")
    thisTech = techModel.objects.get(pk=techId)
    for old_cve in thisTech.cves.all():
        old_cve.isSeen = True
        old_cve.isNew = False
        old_cve.save()


@shared_task
def async_add_new_subdomain(*args):
    domainId = args[0]
    subdomainInfo = args[1]
    async_create_subdomains.delay(domainId, subdomainInfo["name"])
