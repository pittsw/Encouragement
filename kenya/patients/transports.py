from patients.models import SMSSyncOutgoing

class SMSSyncTransport(object):
    """A transport that sends a message through an SMSSync API.

    """

    @classmethod
    def send(cls, target, content):
        """Sends a message through the SMSSync protocol.

        """
        SMSSyncOutgoing(target=target, content=content).save()
