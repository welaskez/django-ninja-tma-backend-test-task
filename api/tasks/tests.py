from unittest.mock import patch

from core.auth.jwt import get_tokens
from django.test import TestCase
from ninja.testing import TestClient
from users.models import User

from .api import router
from .models import Task
from .schemas import TaskCompletedRead


class TasksTest(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create(username="username", balance=150, tg_id=1234)

        self.task_1 = Task.objects.create(
            photo="https://photos.com/some_photo_1",
            name="task 1",
            link="https://t.me/@testchannel",
            reward=1,
            type="telegram",
        )
        self.task_2 = Task.objects.create(
            photo="https://photos.com/some_photo_2",
            name="task 2",
            link="https://youtube.com/watch?=sdafsadf",
            reward=3,
            type="youtube",
        )

        tokens = get_tokens(str(self.user_1.id))
        self.client = TestClient(router, headers={"Authorization": f"Bearer {tokens.access_token}"})

    @patch("tasks.api.check_telegram_subscribe", return_value=True)
    def test_complete_task_telegram(self, mock_check_telegram):
        response = self.client.post(f"/complete/{self.task_1.id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["success"], True)
        self.assertEqual(response.json()["message"], "Task successfully completed")

    @patch("tasks.api.check_telegram_subscribe", return_value=False)
    def test_not_complete_task_telegram(self, mock_check_telegram):
        response = self.client.post(f"/complete/{self.task_1.id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["success"], False)
        self.assertEqual(response.json()["message"], "Task not completed yet")

    def test_complete_task_other(self):
        response = self.client.post(f"/complete/{self.task_2.id}")

        expected_response = TaskCompletedRead(
            success=True,
            task=self.task_2,
            message="Task successfully completed",
        ).model_dump()
        expected_response["task"]["reward"] = f"{expected_response['task']['reward']:.2f}"

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_response)
