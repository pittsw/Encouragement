class BaseTransport(object):
    """The superclass of all transports.

    """

    urls = []
    """Put any urls necessary for the given transport here."""

    @classmethod
    def send(cls, target, content):
        """Subclass this to change send behavior.

        """
        pass
