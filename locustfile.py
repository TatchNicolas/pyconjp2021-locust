import json
import logging

from locust import HttpUser, between, events, task
from locust.runners import MasterRunner
from locust.stats import console_logger
from locust_plugins.users import RestUser

from sample.database import setup_initial_data, teardown_database

# You can supress tables in log by disabling stats logger
console_logger.disabled = True

logger = logging.getLogger(__name__)

with open("users.json", "r") as f:
    USERS = json.load(f)


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    if isinstance(environment.runner, MasterRunner):
        logger.info("Setting up database...")
        setup_initial_data()
        logger.info("Finished setting up database")
    else:
        logger.info("Starting worker setup")
        # Do worker node setup
        logger.info("Finished worker setup")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    if isinstance(environment.runner, MasterRunner):
        logger.info("Tearing down from master")
        teardown_database()
        logger.info("Finished tearing down from master")
    else:
        logger.info("Tearing down from worker")
        # Do worker node setup
        logger.info("Finish tearing down from worker")


class AuthenticatedUser(HttpUser):

    wait_time = between(1, 5)

    def __init__(self, environment):
        self.name = None
        super().__init__(environment)

    def on_start(self):
        if len(USERS) > 0:
            user = USERS.pop()
            logger.info(f"popped user: {user}")
            self.name = user["name"]
            self.client.post(
                "/auth",
                json={
                    "name": user["name"],
                    "password": user["password"],
                },
            )

    @task
    def get_name(self):
        with self.client.get("/") as resp:
            if resp.json()["name"] != self.name:
                logger.warning("not match")
                resp.failure()
