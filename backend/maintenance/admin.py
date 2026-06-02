from django.contrib import admin

from .models import MaintenancePlan, MaintenanceRecord


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ("car", "service_type", "date", "odometer_km", "cost", "created_at")
    list_filter = ("service_type", "date", "car")
    search_fields = ("car__vin", "notes")
    ordering = ("-date", "-odometer_km", "-id")


@admin.register(MaintenancePlan)
class MaintenancePlanAdmin(admin.ModelAdmin):
    list_display = ("car", "service_type", "interval_km", "last_done_km", "updated_at")
    list_filter = ("service_type", "car")
    search_fields = ("car__vin",)
    ordering = ("car__vin", "service_type")
