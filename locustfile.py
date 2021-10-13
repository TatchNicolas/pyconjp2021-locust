import json
import logging

from locust import HttpUser, between, events, task
from locust.runners import MasterRunner
from locust.stats import console_logger
from locust_plugins.users import RestUser

from sample.database import setup_initial_data, teardown

# You can supress tables in log by disabling stats logger
console_logger.disabled = True

logger =logging.getLogger(__name__)

with open("users.json", "r") as f:
    USERS = json.load(f)


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    if isinstance(environment.runner, MasterRunner):
        logger.info("Setting up database...")
        setup_initial_data()
        logger.info("finished")
    else:
        logger.info("Beginning worker setup")
        teardown()
        logger.info("finished")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    if isinstance(environment.runner, MasterRunner):
        logger.info("tearing down from master")
    else:
        logger.info("tearing down from worker")


class AnonymousUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def auth(self):
        with self.client.post(
            "/auth",
            json={"name": "non-existent user", "password": "password1234"},
            catch_response=True,
        ) as resp:
            if resp.status_code == 403:
                resp.success()
            else:
                resp.failure("Should be blocked")

    @task
    def auth(self):
        with self.client.get(
            "/",
            catch_response=True,
        ) as resp:
            if resp.status_code == 403:
                resp.success()
            else:
                resp.failure("Should be blocked")


class ExistingUser(RestUser):
    wait_time = between(1, 5)

    def on_start(self):
        if len(USERS) > 0:
            user = USERS.pop()
            logger.info(f"popped user: {user}")
            self.rest(
                "POST",
                "/auth",
                json={"name": user["name"], "password": user["password"]},
            )

    @task
    def hello_world(self):
        with self.rest("GET", "/") as resp:
            if resp.status_code == 403:
                resp.success()
            else:
                resp.failure()
