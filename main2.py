from proton._reactor import Container

from config import BROKER_URL, QUEUE_NAME
from consumer import ExampleConsumer
from sender import send_message

if __name__ == "__main__":
    try:
        # send 5 message
        for i in range(5):
            send_message(
                url=BROKER_URL,
                queue=QUEUE_NAME,
                body=i
            )

        # consume with 40" sleep
        Container(ExampleConsumer(
            broker_url=BROKER_URL,
            amqp_queue_name=QUEUE_NAME,
            timeout=40)).run()
    except KeyboardInterrupt: pass

