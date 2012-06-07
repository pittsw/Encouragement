from transports import BaseTransport
from smssync.models import SMSSyncOutgoing

class Transport(BaseTransport):
    """A transport that sends a message through an SMSSync API.

    """

    @classmethod
    def send(cls, target, content):
        """Sends a message through the SMSSync protocol.

        """
        SMSSyncOutgoing(target=target, content=content).save()
