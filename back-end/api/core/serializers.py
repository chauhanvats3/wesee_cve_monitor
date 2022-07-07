from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_writable_nested import UniqueFieldsMixin, NestedUpdateMixin, NestedCreateMixin


from .models import Domain, Subdomain, Tech, CVE


class CVESerializer(serializers.ModelSerializer):
    class Meta:
        model = CVE
        fields = "__all__"


class TechSerializer(serializers.ModelSerializer):
    cves = CVESerializer(many=True)

    class Meta:
        model = Tech
        fields = "__all__"


class SubdomainSerializer(serializers.ModelSerializer):
    techs = TechSerializer(many=True)

    class Meta:
        model = Subdomain
        fields = "__all__"


class DomainSerializer(WritableNestedModelSerializer):
    name = serializers.ReadOnlyField()
    protocol = serializers.ReadOnlyField()
    subdomains = SubdomainSerializer(many=True)
    techs = TechSerializer(many=True)

    def get_queryset(self):
        return Domain.objects.all().filter(author=self.request.user)

    class Meta:
        model = Domain
        fields = "__all__"
        read_only_fields = ["author"]
