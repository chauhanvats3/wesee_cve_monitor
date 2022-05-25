from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DomainViewSet, SubdomainViewSet, TechViewSet, CVEViewSet

router = DefaultRouter()
router.register(r"domains", DomainViewSet)
router.register(r"subdomains", SubdomainViewSet)
router.register(r"techs", TechViewSet)
router.register(r"cves", CVEViewSet)

urlpatterns = [path("", include(router.urls))]
