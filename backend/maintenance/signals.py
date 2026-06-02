from django.db.models.signals import post_save
from django.dispatch import receiver

from notifications.broadcast import broadcast_reminders

from .models import MaintenancePlan, MaintenanceRecord


@receiver(post_save, sender=MaintenanceRecord)
def on_maintenance_saved(sender, instance: MaintenanceRecord, created: bool, **kwargs):
    # Keep plan's last_done_km in sync (simple demo logic).
    plan, _ = MaintenancePlan.objects.get_or_create(
        car=instance.car,
        service_type=instance.service_type,
        defaults={"last_done_km": instance.odometer_km},
    )
    if int(instance.odometer_km) > int(plan.last_done_km):
        plan.last_done_km = instance.odometer_km
        plan.save(update_fields=["last_done_km", "updated_at"])

    broadcast_reminders()

