import os
from datetime import date

from dotenv import load_dotenv
from faker import Faker
from locust import HttpUser, between, task

load_dotenv()
fake = Faker()


class TestUser(HttpUser):
    wait_time = between(1, 5)
    host = os.getenv("LOAD_TEST_URL")

    def on_start(self) -> None:
        self.username = fake.user_name()
        self.password = fake.password(length=8)

        self.client.post(
            "/auth/register",
            json={"email": fake.email(), "username": self.username, "password": self.password},
        )

        response = self.client.post(
            "/auth/login",
            json={"username": self.username, "password": self.password},
        )

        self.client.headers["Authorization"] = f"Bearer {response.json()['access_token']}"

        habit = self.client.post(
            "/habits/",
            json={"name": "Exercise", "frequency": "daily"},
        )
        self.habit_id = habit.json()["id"]

    @task(3)
    def list_habits(self) -> None:
        self.client.get("/habits/")

    @task(2)
    def add_completion(self) -> None:
        self.client.post(
            f"/habits/{self.habit_id}/logs",
            json={"logged_at": date.today().isoformat()},
        )

    @task(2)
    def list_stats(self) -> None:
        self.client.get("/stats/summary")
