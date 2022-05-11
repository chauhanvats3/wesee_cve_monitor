from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DomainViewSet,SubdomainViewSet,TechViewSet,CVEViewSet, UserViewSet

router = DefaultRouter()
router.register('domains', DomainViewSet)
router.register('subdomains', SubdomainViewSet)
router.register('techs', TechViewSet)
router.register('cves', CVEViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    path("", include(router.urls))
]