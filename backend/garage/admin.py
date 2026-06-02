from django.contrib import admin

from .models import Car, FuelFillUp, SparePartOrder


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("vin", "make", "model", "owner", "created_at")
    search_fields = ("vin", "make", "model")
    ordering = ("-created_at",)


@admin.register(FuelFillUp)
class FuelFillUpAdmin(admin.ModelAdmin):
    list_display = ("car", "date", "odometer_km", "liters", "total_cost", "created_at")
    list_filter = ("date", "car")
    search_fields = ("car__vin",)
    ordering = ("-date", "-odometer_km", "-id")


@admin.register(SparePartOrder)
class SparePartOrderAdmin(admin.ModelAdmin):
    list_display = ("car", "part_name", "quantity", "status", "vendor", "price", "created_at")
    list_filter = ("status", "car")
    search_fields = ("car__vin", "part_name", "part_number", "vendor")
    ordering = ("-created_at", "-id")
