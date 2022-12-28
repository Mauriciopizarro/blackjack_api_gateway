import time
from threading import Thread
import infrastructure.injector # no remove this dependecy
from infrastructure.event_managers.pass_reset_send_email_listener import PassResetSendEmailListener
from infrastructure.event_managers.user_created_send_email_listener import UserCreatedSendEmailListener


def start():
    time.sleep(25)
    Thread(target=UserCreatedSendEmailListener).start()
    Thread(target=PassResetSendEmailListener).start()


if __name__ == "__main__":
    start()
