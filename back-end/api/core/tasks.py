import random
from socket import timeout
import sys
import time
from celery import shared_task, group
from .utilities import getTechs, getCVEs, findSubdomains, sendCVEmail
from django.apps import apps
from .periodic import periodic_update_domain_CVEs


@shared_task
def async_create_subdomains(domainId, subdomainName):
    domainModel = apps.get_model(app_label="core", model_name="Domain")
    thisDomain = domainModel.objects.get(pk=domainId)
    thisDomain.subdomains.create(name=subdomainName, include=True)
    print("subdomain created : " + subdomainName)


@shared_task
def async_create_domain_tech(domainId, techName, localversions):
    domainModel = apps.get_model(app_label="core", model_name="Domain")
    thisDomain = domainModel.objects.get(pk=domainId)
    randColor = "%06x" % random.randint(0, 0xFFFFFF)
    arr = {"arr": localversions}
    thisDomain.techs.create(
        name=techName,
        versions=arr,
        color=randColor,
        updating_cve=True,
        author=thisDomain.author,
    )
    print("Domain Tech Created : " + techName)


@shared_task
def async_create_subdomain_techs(subdomainId, techName, localVersions):
    subdomainModel = apps.get_model(app_label="core", model_name="Subdomain")
    thisSubdomain = subdomainModel.objects.get(pk=subdomainId)
    thisDomain = list(thisSubdomain.domain_set.all())[0]
    randColor = "%06x" % random.randint(0, 0xFFFFFF)
    arr = {"arr": localVersions}
    thisSubdomain.techs.create(
        name=techName,
        versions=arr,
        color=randColor,
        updating_cve=True,
        author=thisDomain.author,
    )
    print("Saved Subdomain Techs : " + thisSubdomain.name)


def saveSubdomains(thisDomain):
    subdomainsResponse = findSubdomains(thisDomain.name)
    try:
        time.sleep(6)
        subdomain_create_group = group(
            [
                async_create_subdomains.s(thisDomain.id, subdomain)
                for subdomain in subdomainsResponse
            ]
        )
        print("Group Created")
        group_job = subdomain_create_group.apply_async()
        finished = False
        print("Group Running")
        while not finished:
            finished = group_job.ready()

        print("Group Finished")

        thisDomain.fetching_subdomains = False
        thisDomain.save(update_fields=["fetching_subdomains"])

        print("Subdomains fetched for : " + thisDomain.name)
    except AttributeError as err:
        print(err)
        thisDomain.fetching_subdomains = False
        thisDomain.save(update_fields=["fetching_subdomains"])
        print("Subdomains Not Found")


def saveTechs(thisDomain):
    techResponse = getTechs(thisDomain.full_name)
    try:
        for tech in techResponse[0]["technologies"]:
            techName = tech["name"]
            versions = tech["versions"]
            time.sleep(6)
            async_create_domain_tech.delay(thisDomain.id, techName, versions)
            print("Saved Domain Techs : " + thisDomain.name)

    except:
        print("Some Error Occurred in getting Tech")


@shared_task
def async_get_domain_data(domainId):
    domainModel = apps.get_model(app_label="core", model_name="Domain")
    thisDomain = domainModel.objects.get(pk=domainId)
    if thisDomain.saved_already == False and thisDomain.verified:

        thisDomain.saved_already = True
        thisDomain.save(update_fields=["saved_already"])

        print("Getting Domain Techs : " + thisDomain.name)
        saveTechs(thisDomain)

        print("Getting Subdomains : " + thisDomain.name)
        saveSubdomains(thisDomain)

        periodic_update_domain_CVEs(domainId, thisDomain.cron_interval, thisDomain.name)

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
    TechModel = apps.get_model(app_label="core", model_name="Tech")
    thisTech = TechModel.objects.get(pk=techId)
    thisTech.updating_cve = True
    thisTech.save()


@shared_task
def async_update_domain_cve(*args):
    domainId = args[0]
    domainModel = apps.get_model(app_label="core", model_name="Domain")
    thisDomain = domainModel.objects.get(pk=domainId)
    if thisDomain.verified:
        print("Updating CVEs for : " + thisDomain.name)
        update_tasks = []
        newCVEsIn = []
        for tech in thisDomain.techs.all():
            update_tasks.append(
                {
                    "id": tech.id,
                    "name": tech.name,
                    "domain": thisDomain.name,
                    "subdomain": False,
                }
            )
        for subdomain in thisDomain.subdomains.all():
            for tech in subdomain.techs.all():
                update_tasks.append(
                    {
                        "id": tech.id,
                        "name": tech.name,
                        "domain": thisDomain.name,
                        "subdomain": subdomain.name,
                    }
                )
        update_group = group(
            [async_get_tech_cves.s(tech["id"], True) for tech in update_tasks]
        )
        update_job = update_group.apply_async()
        finished = False
        while not finished:
            finished = update_job.ready()
        update_res = update_job.get()
        for index, tech in enumerate(update_tasks):
            if update_res[index]:
                newCVEsIn.append(update_tasks[index])
        print("New CVEs were found")
        async_compose_cve_mail.delay(newCVEsIn)
    else:
        print(f"{thisDomain.name} is not verified")


@shared_task
def async_get_tech_cves(techId, directly):
    techModel = apps.get_model(app_label="core", model_name="Tech")
    thisTech = techModel.objects.get(pk=techId)
    oldCVEs = []
    hasNewCVE = False
    if thisTech.updating_cve is True or directly:
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
                else:
                    hasNewCVE = True
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
        return hasNewCVE
    else:
        print("Not Updating CVEs")


@shared_task
def async_mark_cve_seen(techId):
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


@shared_task
def async_compose_cve_mail(newCVEsIn):
    techModel = apps.get_model(app_label="core", model_name="Tech")
    techObj = techModel.objects.get(pk=newCVEsIn[0]["id"])
    author = techObj.author
    recepient = author.email
    domain = newCVEsIn[0]["domain"]

    subject = "New CVEs Found for : " + domain
    body = f"Hello {author.first_name}!<br/> Some New CVEs have been found for <strong><a href='http://104.248.175.4:3000/dashboard/{domain}'>{domain}</a></strong> : <br/>"

    index = 1
    for tech in newCVEsIn:
        # thisTech = techModel.objects.get(pk=tech["id"])
        if not tech["subdomain"]:
            body += f"{index}: {tech['domain']} -> {tech['name']}<br/>"
            index += 1
        else:
            body += f"{index}: {tech['domain']} -> {tech['subdomain']} --> {tech['name']}<br/>"
            index += 1
    body += f"<br/>Regards,<br/>Team WeSeeCVEs!"

    sendCVEmail({"recepient": recepient, "subject": subject, "body": body})
