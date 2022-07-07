import json
from django.db.models import Count
from django.apps import apps


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
)
from .utilities import verifyDomain
from .models import Domain, Subdomain, Tech, CVE
from .tasks import (
    async_mark_cve_seen,
    async_add_new_subdomain,
)


class DomainViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = DomainSerializer
    queryset = Domain.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        query_set = self.queryset.filter(author=self.request.user)
        verified = query_set.filter(verified=True).defer("author")
        unverified = (
            query_set.filter(verified=False)
            .only("full_name", "verified", "verify_code", "photo", "author")
            .defer("author")
        )
        return verified | unverified

    @action(detail=True, methods=["post"])
    def verify(self, request, pk):
        print("Verify initiated")
        thisDomain = self.get_object()
        thisObject = serializers.serialize(
            "json",
            [
                thisDomain,
            ],
        )
        struct = json.loads(thisObject)[0]
        fullName = struct["fields"]["full_name"]
        verificationNumber = struct["fields"]["verify_code"]
        name = fullName.split("://")[1]
        isVerified = verifyDomain(name, verificationNumber)
        if isVerified == True:
            data_to_change = {"verified": "true"}
        else:
            return Response({"status": 400, "error": "Could Not Verify. Try Later!"})
        # Partial update of the data
        serializer = DomainSerializer(thisDomain, data=data_to_change, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)

        return Response({"status": 200, "message": "Domain is verified"})

    @action(detail=True, methods=["post"])
    def addNewSubdomain(self, request, pk):
        async_add_new_subdomain.delay(pk, request.data)
        return Response({"status": 200, "message": "Subomain Will Be added for sure"})


class SubdomainViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = SubdomainSerializer
    queryset = Subdomain.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.annotate(q_count=Count("techs")).order_by("-q_count")
        return query_set

    @action(detail=True, methods=["post"])
    def findTech(self, request, pk):
        SubdomainModel = apps.get_model(app_label="core", model_name="Subdomain")
        thisSubdomain = SubdomainModel.objects.get(pk=pk)
        thisSubdomain.techs_fetched = False
        thisSubdomain.save()
        return Response("Updating Subdomain Techs")


class TechViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TechSerializer
    queryset = Tech.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        print(type(self))
        return self.queryset.filter(author=self.request.user).defer("author")

    @action(detail=True, methods=["post"])
    def markCVEsSeen(self, request, pk):
        async_mark_cve_seen.delay(pk)
        return Response("Marking CVEs as Seen")


class CVEViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CVESerializer
    queryset = CVE.objects.all()
