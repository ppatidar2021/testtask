from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import UserTask
from .tasks import process_csv_data
from .serializers import UserTaskSerializer


def login_view(request):
    return render(request, "process/login.html")


def index(request):
    return render(request, "process/index.html")


class ProcessDataView(APIView):
    """
    API view to start processing CSV data and create a UserTask record.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        user_task_obj = UserTask.objects.filter(
            user_id=user_id, is_completed=False
        ).first()

        if user_task_obj:
            return self._create_task_response(
                user_id, user_task_obj.task_id, create=False
            )

        task_result = process_csv_data.delay()
        return self._create_task_response(user_id, task_result.id)

    def _create_task_response(self, user_id, task_id, create=True):
        user_task_data = {
            "user": user_id,
            "task_id": task_id,
        }

        serializer = UserTaskSerializer(data=user_task_data)
        if serializer.is_valid():
            if create:
                serializer.save()
                status_code = status.HTTP_201_CREATED
                data = serializer.data
            else:
                status_code = status.HTTP_200_OK
                data = {**user_task_data, "is_completed": False}
            return Response(data, status=status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProcessStatusView(APIView):
    """
    API view to check the status of the user's last processed task.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_task = UserTask.objects.filter(user=request.user).last()
        is_completed = user_task.is_completed if user_task else True
        return Response({"completed": is_completed}, status=status.HTTP_200_OK)
