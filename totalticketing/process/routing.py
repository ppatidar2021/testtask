from django.urls import path

from . import consumers


websocket_urlpatterns = [
    path("ws/consumer_path/<str:task_id>/", consumers.TaskStatusConsumer.as_asgi()),
]
