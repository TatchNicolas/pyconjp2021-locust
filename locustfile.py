import time
import logging
import uuid

from locust import HttpUser, task, between, events
from locust.runners import MasterRunner


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    if not isinstance(environment.runner, MasterRunner):
        logging.info("Beginning test setup")
    else:
        logging.info("Started test from Master node")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    if not isinstance(environment.runner, MasterRunner):
        logging.info("Cleaning up test data")
    else:
        logging.info("Stopped test from Master node")


class LoadTestUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def hello_world(self):
        self.client.get("/")

    # @task(3)
    # def view_items(self):
    #     for item_id in range(10):
    #         self.client.get(f"/item?id={item_id}", name="/item")
    #         time.sleep(1)

    def on_start(self):
        user_id = str(uuid.uuid4())
        self.client.post("/login", json={"user_id": user_id, "password":"password"})
 