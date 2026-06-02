import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from garage.models import Car, FuelFillUp
from maintenance.models import MaintenancePlan


def build_reminders(*, due_soon_threshold_km: int = 500) -> list[dict]:
    reminders: list[dict] = []
    for car in Car.objects.select_related("owner").all():
        last_fill = (
            FuelFillUp.objects.filter(car=car)
            .order_by("-odometer_km", "-date", "-id")
            .only("odometer_km")
            .first()
        )
        current_km = int(last_fill.odometer_km) if last_fill else None
        if current_km is None:
            continue

        for plan in MaintenancePlan.objects.filter(car=car):
            next_due = plan.next_due_km
            remaining = next_due - current_km
            overdue = remaining <= 0
            due_soon = (not overdue) and remaining <= due_soon_threshold_km
            if not (overdue or due_soon):
                continue

            reminders.append(
                {
                    "vin": car.vin,
                    "make": car.make,
                    "model": car.model,
                    "owner": car.owner.username,
                    "service_type": plan.service_type,
                    "current_km": current_km,
                    "next_due_km": int(next_due),
                    "remaining_km": int(remaining),
                    "overdue": bool(overdue),
                    "due_soon": bool(due_soon),
                }
            )
    return reminders


class RemindersConsumer(WebsocketConsumer):
    group_name = "maintenance_reminders"

    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.send(
            text_data=json.dumps(
                {
                    "type": "reminders",
                    "items": build_reminders(),
                }
            )
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)

    def reminders_update(self, event):
        self.send(text_data=json.dumps({"type": "reminders", "items": event["items"]}))

