from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_writable_nested import UniqueFieldsMixin, NestedUpdateMixin

from .models import Domain, Subdomain, Tech, CVE, User


class CVESerializer(serializers.ModelSerializer):
    class Meta:
        model = CVE
        fields = "__all__"
        depth = 1


class TechSerializer(UniqueFieldsMixin, WritableNestedModelSerializer):
    cves = CVESerializer(many=True)

    class Meta:
        model = Tech
        fields = "__all__"
        depth = 3


class SubdomainSerializer(UniqueFieldsMixin, WritableNestedModelSerializer):
    techs = TechSerializer(many=True)

    class Meta:
        model = Subdomain
        fields = "__all__"
        depth = 3


class DomainSerializer(UniqueFieldsMixin, WritableNestedModelSerializer):
    name = serializers.ReadOnlyField()
    protocol = serializers.ReadOnlyField()
    subdomains = SubdomainSerializer(many=True)
    techs = TechSerializer(many=True)

    class Meta:
        model = Domain
        fields = "__all__"
        depth = 5


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("domains", "email")
