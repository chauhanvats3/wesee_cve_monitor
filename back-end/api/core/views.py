import json
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core import serializers
from .lookupDNS import verifyDomain
from .serializers import (
    DomainSerializer,
    SubdomainSerializer,
    TechSerializer,
    CVESerializer,
    UserSerializer,
)
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

        struct = json.loads(thisObject)[0]
        fullName = struct["fields"]["full_name"]
        verificationNumber = struct["fields"]["verify_code"]
        name = fullName.split("://")[1]
        isVerified = verifyDomain(name, verificationNumber)
        return HttpResponse(isVerified)
        # return Response(thisDomain)


class SubdomainViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = SubdomainSerializer
    queryset = Subdomain.objects.all()


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
