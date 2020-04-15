import threading
from queue import Queue
from time import sleep

from proton._reactor import EventInjector, ApplicationEvent
from proton.handlers import MessagingHandler


class ExampleConsumer(MessagingHandler):
    def __init__(self, broker_url, amqp_queue_name, timeout):
        super().__init__(auto_accept=False)  # it's important that auto_accept is disabled.
        self.broker_url = broker_url
        self.amqp_queue_name = amqp_queue_name
        self.timeout = timeout

        self.queue = Queue()

        self.injector = EventInjector()

        self.thread = threading.Thread(target=self._process, daemon=True)
        self.thread.start()

    def on_start(self, event):
        event.container.selectable(self.injector)

        self.container = event.container
        self.conn = event.container.connect(url=self.broker_url)
        self.receiver = event.container.create_receiver(self.conn, self.amqp_queue_name)
        print('listening for new messages on /' + self.amqp_queue_name)

    def on_message(self, event):
        # just add the event to our internal thread-safe queue, and give control back to qpid reactor,
        # without accepting the message just yet.
        self.queue.put(event)

    def _process(self):
        """
        Consume queue items, process them, and trigger an event for the main thread to catch and accept/reject the delivery.
        """
        while True:
            event = self.queue.get(True)  # blocks the thread until there's an item to process

            print('job received: ' + str(event.message.body))
            print('sleeping ' + str(self.timeout) + ' seconds')
            sleep(self.timeout)
            print('done sleeping')
            print('job processed successfully')

            # once the event is processed, trigger a custom application-event.
            self.injector.trigger(ApplicationEvent("message_handled", delivery=event.delivery, subject=event.message.body))

            # notify the queue that the task has been processed
            self.queue.task_done()

    def on_message_handled(self, event):
        """
        Capture event triggered from the worker thread in order to ack the message accordingly
        This could be unfolded into accept/reject events if needed, just accepting it here.
        """
        self.accept(event.delivery)
        print('job accepted: ' + str(event.subject))

    def on_connection_error(self, event):
        print('connection_error', event.connection.condition, event.connection.remote_condition)
