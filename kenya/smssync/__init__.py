from transports import BaseTransport
from smssync.models import SMSSyncOutgoing

class Transport(BaseTransport):
    """A transport that sends a message through an SMSSync API.

    """

    @classmethod
    def send(cls, client, content):
        """Sends a message through the SMSSync protocol.

        """
        SMSSyncOutgoing(target=client.phone_number, content=content).save()
