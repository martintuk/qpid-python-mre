from proton import Message
from proton._utils import BlockingConnection


def send_message(url, queue, body):
    conn = BlockingConnection(url)
    sender = conn.create_sender(queue)
    sender.send(Message(body=body))
