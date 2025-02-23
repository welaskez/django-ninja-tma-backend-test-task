from ninja import ModelSchema, Schema

from tasks.models import Task


class TaskRead(ModelSchema):
    class Meta:
        model = Task
        fields = "__all__"


class TaskCompletedRead(Schema):
    success: bool
    task: TaskRead
    message: str
