from datetime import date, timedelta

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

        delta = timedelta(days=30)
        self.reg_client.birth_date = date.today() - delta
        self.hbp_client.birth_date = date.today() - delta
        self.reg_client.save()
        self.hbp_client.save()

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


class TestUpdate(TestCase):
    """This class tests to make sure that clients update properly when a new
    message is received.

    """

    fixtures = ['test_pending']

    def setUp(self):
        self.reg_client = Client.objects.all()[0]
        self.nurse = Nurse.objects.all()[0]
        self.msg = Message.objects.create(
            client_id=self.reg_client,
            user_id=self.nurse,
            sent_by='Client',
            content='Test',
        )

    def test_last_msg(self):
        """Test that send time of the last message is updated.
        
        """
        self.assertEqual(self.reg_client.last_msg, self.msg.date)

    def test_pending(self):
        """Test that the pending messages counter is incremented.

        """
        self.assertEqual(self.reg_client.pending, 1)

    def test_pending_restarts(self):
        """Test that when you mark a message as read, the client's
        counter decrements.

        """
        self.msg.read = True
        self.msg.save()
        num_pending = self.reg_client.pending
        self.msg.read = False # restart our state
        self.msg.save()
        self.assertEqual(num_pending, 0)
