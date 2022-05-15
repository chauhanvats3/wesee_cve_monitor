from rest_framework import serializers
from .models import Domain, Subdomain, Tech, CVE, User


class DomainSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()
    protocol = serializers.ReadOnlyField()

    class Meta:
        model = Domain
        fields = "__all__"
        depth = 5
        read_only_fields = ("verified",)


class SubdomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subdomain
        fields = "__all__"
        depth = 3


class TechSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tech
        fields = "__all__"
        depth = 3


class CVESerializer(serializers.ModelSerializer):
    class Meta:
        model = CVE
        fields = "__all__"
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("domains", "email")
