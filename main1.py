from proton.reactor import Container

from config import BROKER_URL, QUEUE_NAME
from consumer import ExampleConsumer
from sender import send_message

if __name__ == "__main__":
    try:
        # send 1 message
        send_message(
            url=BROKER_URL,
            queue=QUEUE_NAME
        )

        # consume with 60" sleep
        Container(ExampleConsumer(
            broker_url=BROKER_URL,
            queue=QUEUE_NAME,
            timeout=60)).run()
    except KeyboardInterrupt: pass

