from django.test import TestCase

from patients.models import *
from patients.tasks import scheduled_message


class TestTrains(TestCase):
    """This class is where all tests involving the automated messages go.
    
    """

    fixtures = ['test_train']

    def setUp(self):
        self.reg_client = Client.objects.get(pk=100)
        self.hbp_client = Client.objects.get(pk=101)
        for i in range(3):
            # We need to call scheduled_message by hand to avoid race conditions
            scheduled_message(self.reg_client)
            scheduled_message(self.hbp_client)

    def tearDown(self):
        pass

    def test_condition(self):
        """Test to make sure that conditions are respected.

        """
        reg_msg = Message.objects.filter(client_id=self.reg_client)[0]
        hbp_msg = Message.objects.filter(client_id=self.hbp_client)[0]
        self.assertEqual(reg_msg.content, "Third trimester message!")
        self.assertEqual(hbp_msg.content, "Blood pressure message one!")

    def test_no_repeat(self):
        """Test to make sure that messages marked to not repeat don't.

        """
        reg_msg = Message.objects.filter(client_id=self.reg_client)[1]
        hbp_msg = Message.objects.filter(client_id=self.hbp_client)[1]
        self.assertEqual(reg_msg.content, "Generalized pregnancy message!")
        self.assertEqual(hbp_msg.content, "Blood pressure message two!")

    def test_repeat(self):
        """Test to make sure that messages marked to repeat do.

        """
        reg_msg = Message.objects.filter(client_id=self.reg_client)[2]
        hbp_msg = Message.objects.filter(client_id=self.hbp_client)[2]
        self.assertEqual(reg_msg.content, "Generalized pregnancy message!")
        self.assertEqual(hbp_msg.content, "Third trimester message!")
