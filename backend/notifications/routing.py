from django.urls import re_path

from .consumers import RemindersConsumer

websocket_urlpatterns = [
    re_path(r"^ws/reminders/$", RemindersConsumer.as_asgi()),
]

