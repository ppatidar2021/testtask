import time
import pandas as pd
from asgiref.sync import async_to_sync

from celery import shared_task
from channels.layers import get_channel_layer

from .models import UserTask


@shared_task(bind=True)
def process_csv_data(self):
    task_id = self.request.id
    df = pd.read_csv("data/csv/customers-100.csv")
    channel_layer = get_channel_layer()
    group_name = f"task_{task_id}"

    # Process each row in the CSV file
    for index, row in df.iterrows():
        time.sleep(1)

        # Send progress updates to the WebSocket group
        async_to_sync(channel_layer.group_send)(
            group_name,
            {"type": "send_message", "progress_data": f"Processing row {index}"},
        )

    try:
        user_task = UserTask.objects.get(task_id=task_id)
        user_task.is_completed = True
        user_task.save()
    except UserTask.DoesNotExist:
        print(f"UserTask with task_id {task_id} not found.")

    return "Task completed"
