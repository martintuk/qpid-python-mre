from time import sleep

from proton.handlers import MessagingHandler


class ExampleConsumer(MessagingHandler):
    def __init__(self, broker_url, amqp_queue_name, timeout):
        super().__init__()
        self.broker_url = broker_url
        self.amqp_queue_name = amqp_queue_name
        self.timeout = timeout

    def on_start(self, event):
        self.container = event.container
        self.conn = event.container.connect(url=self.broker_url)
        self.receiver = event.container.create_receiver(self.conn, self.amqp_queue_name)
        print('listening for new messages on /' + self.amqp_queue_name)

    def on_message(self, event):
        print('job received')
        print('sleeping ' + str(self.timeout) + ' seconds')
        sleep(self.timeout)
        print('done sleeping')
        print('job processed successfully')

    def on_connection_error(self, event):
        print('connection_error', event.connection.condition, event.connection.remote_condition)
