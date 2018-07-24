from time import sleep
from channels.consumer import SyncConsumer

class BackgroundTaskConsumer(SyncConsumer):
    def task_a(self, message):
        sleep(5)

    def task_b(self, message):
        sleep(message['wait'])