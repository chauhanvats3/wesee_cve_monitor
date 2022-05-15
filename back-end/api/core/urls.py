from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DomainViewSet, SubdomainViewSet, TechViewSet, CVEViewSet, UserViewSet

router = DefaultRouter()
router.register(r"domains", DomainViewSet)
router.register(r"subdomains", SubdomainViewSet)
router.register(r"techs", TechViewSet)
router.register(r"cves", CVEViewSet)
router.register(r"users", UserViewSet)

urlpatterns = [path("", include(router.urls))]
