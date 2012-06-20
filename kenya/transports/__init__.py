class BaseTransport(object):
    """The superclass of all transports.

    """

    urls = []
    """Put any urls necessary for the given transport here."""

    @classmethod
    def send(cls, target, content):
        """Sends a single message containing content to target.

        Arguments:
            target - the desination (string)
            content - the body of the message (string)

        """
        pass

    @classmethod
    def send_batch(cls, lst):
        """Sends all of the messages in lst.

        Arguments:
            lst - a list of (target, content) tuples like those that could be
                sent with send()

        """
        for target, content in lst:
            send(target, content)
