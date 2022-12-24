import time
import infrastructure.injector # no remove this dependecy
from infrastructure.event_managers.send_email_listener import SendEmailListener


def start_consumer():
    time.sleep(25)
    send_email_listener = SendEmailListener()
    send_email_listener.start_consuming()


if __name__ == "__main__":
    start_consumer()
