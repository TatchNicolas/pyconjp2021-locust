import logging

from locust import HttpUser, between, events, task
from locust.runners import MasterRunner
from locust.stats import console_logger
from locust_plugins.users import RestUser

# You can supress tables in log by disabling stats logger
console_logger.disabled = True


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    if not isinstance(environment.runner, MasterRunner):
        logging.info("Beginning test setup")
    else:
        logging.info("Started test from Master node")
        logging.info("Setting up database...")
        logging.info("finished")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    if not isinstance(environment.runner, MasterRunner):
        logging.info("Cleaning up test data")
    else:
        logging.info("Stopped test from Master node")


class AnonymousUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def hello_world(self):
        with self.client.post(
            "/auth",
            json={"name": "non-existent user", "password": "password1234"},
            catch_response=True,
        ) as resp:
            if resp.status_code == 403:
                resp.success()
            else:
                resp.failure()


class ExistingUser(RestUser):
    wait_time = between(1, 5)

    @task
    def hello_world(self):
        with self.client.post(
            "/auth",
            json={"name": "non-existent user", "password": "password1234"},
            catch_response=True,
        ) as resp:
            if resp.status_code == 403:
                resp.success()
            else:
                resp.failure()
