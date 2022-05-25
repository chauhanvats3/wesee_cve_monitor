from django.contrib import admin
from .models import Domain, Subdomain, Tech, CVE


# Register your models here.
admin.site.register(Domain)
admin.site.register(Subdomain)
admin.site.register(Tech)
admin.site.register(CVE)
