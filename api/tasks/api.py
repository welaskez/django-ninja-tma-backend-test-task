import asyncio
import time

from django.shortcuts import get_object_or_404
from ninja.router import Router
from users.models import User

from tasks.models import Task
from tasks.schemas import TaskCompletedRead, TaskRead
from tasks.utils import check_telegram_subscribe

router = Router()


@router.get("", response=list[TaskRead])
def get_tasks(request):
    return Task.objects.all()


@router.post("complete/{task_id}", response=TaskCompletedRead)
def complete_task(request, task_id: int):
    task = get_object_or_404(Task, id=task_id)
    user = get_object_or_404(User, id=request.auth.id)

    if task in user.tasks.all():
        return TaskCompletedRead(success=False, task=task, message="Task already completed")

    if task.type == "telegram":
        completed = asyncio.run(check_telegram_subscribe(link=task.link, tg_id=user.tg_id))
    else:
        completed = True
        time.sleep(3)

    if completed:
        msg = "Task successfully completed"
        user.tasks.add(task)
        user.balance += task.reward
        user.save()
    else:
        msg = "Task not completed yet"

    return TaskCompletedRead(success=completed, task=task, message=msg)
