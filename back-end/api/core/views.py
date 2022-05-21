from crypt import methods
import random
import json

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core import serializers
from .serializers import (
    DomainSerializer,
    SubdomainSerializer,
    TechSerializer,
    CVESerializer,
    UserSerializer,
)
from .utilities import findSubdomains, getCVEs, getPhoto, getTechs, verifyDomain
from .models import Domain, Subdomain, Tech, CVE, User


class DomainViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = DomainSerializer
    queryset = Domain.objects.all()

    @action(detail=True, methods=["post"])
    def verify(self, request, pk):
        thisDomain = self.get_object()
        thisObject = serializers.serialize(
            "json",
            [
                thisDomain,
            ],
        )
        print(thisObject)
        struct = json.loads(thisObject)[0]
        fullName = struct["fields"]["full_name"]
        verificationNumber = struct["fields"]["verify_code"]
        name = fullName.split("://")[1]
        isVerified = verifyDomain(name, verificationNumber)
        if isVerified:
            data_to_change = {"verified": "true"}
        else:
            return Response({"status": 400, "error": "Could Not Verify"})
        # Partial update of the data
        serializer = DomainSerializer(thisDomain, data=data_to_change, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)

        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def enumSubdomains(self, request, pk):
        thisDomain = self.get_object()
        thisObject = serializers.serialize(
            "json",
            [
                thisDomain,
            ],
        )
        print(thisObject)
        struct = json.loads(thisObject)[0]
        fullName = struct["fields"]["full_name"]
        name = fullName.split("://")[1]
        jawab = findSubdomains(name)
        newSubdomains = []
        try:
            for subdomain in jawab["FDNS_A"]:
                useful = subdomain.split(",")[1]
                print(useful)
                newSubdomains.append({"techs": [], "name": useful, "include": "true"})
        except:
            newSubdomains = []
        data_to_change = {"subdomains": newSubdomains}
        serializer = DomainSerializer(thisDomain, data=data_to_change, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def findTech(self, request, pk):
        thisDomain = self.get_object()
        thisObject = serializers.serialize(
            "json",
            [
                thisDomain,
            ],
        )
        struct = json.loads(thisObject)[0]
        fullName = struct["fields"]["full_name"]
        response = getTechs(fullName)
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
        return Response(data_to_change)

    @action(detail=True, methods=["post"])
    def getPhoto(self, request, pk):
        thisDomain = self.get_object()
        thisObject = serializers.serialize(
            "json",
            [
                thisDomain,
            ],
        )
        print(thisObject)
        struct = json.loads(thisObject)[0]
        fullName = struct["fields"]["full_name"]
        verificationNumber = struct["fields"]["verify_code"]
        name = fullName.split("://")[1]
        photoUrl = getPhoto()
        data_to_change = {"photo": photoUrl}
        serializer = DomainSerializer(thisDomain, data=data_to_change, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
        return Response(serializer.data)


class SubdomainViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = SubdomainSerializer
    queryset = Subdomain.objects.all()

    @action(detail=True, methods=["post"])
    def findTech(self, request, pk):
        thisSubdomain = self.get_object()
        thisObject = serializers.serialize(
            "json",
            [
                thisSubdomain,
            ],
        )
        struct = json.loads(thisObject)[0]
        subDomain = struct["fields"]["name"]
        response = getTechs(subDomain)
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
        serializer = SubdomainSerializer(
            thisSubdomain, data=data_to_change, partial=True
        )
        if serializer.is_valid():
            self.perform_update(serializer)
        return Response(serializer.data)


class TechViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TechSerializer
    queryset = Tech.objects.all()


class CVEViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CVESerializer
    queryset = CVE.objects.all()


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
