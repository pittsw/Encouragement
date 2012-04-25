import logging

class BaseTransport(object):
    """While it is not necessary to subclass BaseTransport, it is a good model
    for how to properly write a transport.

    """

    logger = logging.getLogger('transports.BaseTransport')

    @classmethod
    def send(cls, client, **kwargs):
        cls.logger.info("Sending a message to {client} with kwargs {kwargs}".
            format(client=client, kwargs=kwargs))

    @classmethod
    def poll(cls, **kwargs):
        cls.logger.info("Polling with kwargs {kwargs}".format(kwargs=kwargs))
