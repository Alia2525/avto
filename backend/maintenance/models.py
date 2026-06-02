from django.db import models

from garage.models import Car


class MaintenanceRecord(models.Model):
    class ServiceType(models.TextChoices):
        OIL = "oil", "Oil change"
        INSPECTION = "inspection", "Inspection"
        BRAKES = "brakes", "Brakes"
        OTHER = "other", "Other"

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="maintenance_records")
    service_type = models.CharField(max_length=32, choices=ServiceType.choices, default=ServiceType.OTHER)
    date = models.DateField()
    odometer_km = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-odometer_km", "-id"]

    def __str__(self) -> str:
        return f"{self.car.vin} {self.service_type} {self.odometer_km}km"


class MaintenancePlan(models.Model):
    """
    Planned service rule per car.
    `interval_km` - how often it should be done.
    `last_done_km` - last mileage when the service was completed.
    """

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="maintenance_plans")
    service_type = models.CharField(max_length=32, choices=MaintenanceRecord.ServiceType.choices)
    interval_km = models.PositiveIntegerField(default=10_000)
    last_done_km = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("car", "service_type")]

    @property
    def next_due_km(self) -> int:
        return int(self.last_done_km + self.interval_km)

    def __str__(self) -> str:
        return f"{self.car.vin} {self.service_type} every {self.interval_km}km"
