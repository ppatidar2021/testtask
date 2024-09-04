from celery.result import AsyncResult


def check_task_status(task_id):
    """
    Checks the status of a Celery task based on its task ID.

    Args:
        task_id (str): The ID of the Celery task to check.

    Returns:
        dict: A dictionary containing the task ID, status, result, and readiness.
    """
    result = AsyncResult(task_id)

    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result,
        "ready": result.ready(),
    }
