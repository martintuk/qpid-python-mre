from proton.reactor import Container

from config import BROKER_URL, QUEUE_NAME
from sender import Send

if __name__ == "__main__":
    try:
        Container(Send(
            url=BROKER_URL,
            queue=QUEUE_NAME,
            messages=1)).run()
    except KeyboardInterrupt: pass
