import random
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .getTechs import getTechs

from .models import Domain, Subdomain

""" 
@receiver(pre_save, sender=Subdomain)
def addTechs(sender, instance, **kwargs):
    print(instance.techs)
    response = getTechs(instance.name)
    techs_to_add = []
    try:
        response = response[0]["technologies"]
    except:
        print("No Technologies Found!")
        return """
    """   response = getTechs(fullName)
        techs = []
        for tech in response[0]["technologies"]:
            randColor = "%06x" % random.randint(0, 0xFFFFFF)
            techs.append(
                {
                    "name": tech["name"],
                    "versions": {"arr": tech["versions"]},
                    "cves": [],
                    "color": randColor,
                }
            )
        data_to_change = {"techs": techs}
        serializer = DomainSerializer(thisDomain, data=data_to_change, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
        return Response(data_to_change) """

    """ for tech in response:
        randColor = "%06x" % random.randint(0, 0xFFFFFF)
        techs_to_add.append(
            {
                "name": tech["name"],
                "versions": {"arr": tech["versions"]},
                "cves": [],
                "color": randColor,
            }
        )
    print(techs_to_add) """
    
