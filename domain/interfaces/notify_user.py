from abc import ABC, abstractmethod


class NotifyUser(ABC):

    @abstractmethod
    def send_email(self, user_email, subject, body):
        pass
