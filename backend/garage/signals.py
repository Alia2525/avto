from django.db.models.signals import post_save
from django.dispatch import receiver

from notifications.broadcast import broadcast_reminders

from .models import FuelFillUp


@receiver(post_save, sender=FuelFillUp)
def on_fillup_saved(sender, instance: FuelFillUp, **kwargs):
    broadcast_reminders()

