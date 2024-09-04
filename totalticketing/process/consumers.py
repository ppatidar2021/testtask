import json
import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer

from .utils import check_task_status


class TaskStatusConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.task_id = self.scope["url_route"]["kwargs"]["task_id"]
        self.group_name = f"task_{self.task_id}"

        # Add the WebSocket to the task's group
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        # Accept the WebSocket connection
        await self.accept()

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            if data.get("action") == "check_task_status":
                await self.handle_task_status_check(data["task_id"])
        except (KeyError, json.JSONDecodeError) as e:
            await self.send(json.dumps({"error": str(e)}))

    async def handle_task_status_check(self, task_id):
        task_status = check_task_status(task_id)

        while not task_status["ready"]:
            await asyncio.sleep(1)
            task_status = check_task_status(task_id)
            await self.send(json.dumps({**task_status, "action": "check_task_status"}))

        # Send the final task status
        await self.send(json.dumps(task_status))

    async def send_message(self, event):
        progress_data = event.get("progress_data", {})

        # Send progress data to WebSocket
        await self.send(json.dumps(progress_data))
