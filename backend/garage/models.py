from django.db import models
from django.conf import settings

class Car(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cars",
        null=True,
        blank=True,
    )
    vin = models.CharField(max_length=17, unique=True)
    make = models.CharField(max_length=64)
    model = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        label = f"{self.make}".strip()
        if self.model:
            label = f"{label} {self.model}".strip()
        return f"{label} ({self.vin})".strip()


class FuelFillUp(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="fuel_fillups")
    date = models.DateField()
    odometer_km = models.PositiveIntegerField()
    liters = models.DecimalField(max_digits=7, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-odometer_km", "-id"]

    def __str__(self) -> str:
        return f"{self.car.vin} {self.date} {self.odometer_km}km"


class SparePartOrder(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        ORDERED = "ordered", "Ordered"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="spare_part_orders")
    part_name = models.CharField(max_length=128)
    part_number = models.CharField(max_length=64, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.DRAFT)
    vendor = models.CharField(max_length=128, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ordered_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self) -> str:
        return f"{self.car.vin} {self.part_name} x{self.quantity}"
