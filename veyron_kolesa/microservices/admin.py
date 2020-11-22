from django.contrib import admin
from veyron_kolesa.microservices.models import Service


class ServiceAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "host", "url"]
    readonly_fields = ["name", "host", "url"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Service, ServiceAdmin)
