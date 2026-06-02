from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .consumers import build_reminders


def broadcast_reminders() -> None:
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return

    async_to_sync(channel_layer.group_send)(
        "maintenance_reminders",
        {
            "type": "reminders.update",
            "items": build_reminders(),
        },
    )

