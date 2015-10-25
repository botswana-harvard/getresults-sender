from django.test import TestCase

from getresults_order.configure import Configure as ConfigureOrder
from getresults_sender.configure import Configure as ConfigureSender
from getresults_sender.models import Sender, SenderPanelItem, SenderPanel


class TestGetresults(TestCase):

    def setUp(self):
        configure_order = ConfigureOrder()
        configure_order.load_all()
        configure_sender = ConfigureSender()
        configure_sender.load_all()

    def test_find_sender_panel_items_from_serial_number(self):
        serial_number = 'E12334567890'
        sender = Sender.objects.get(serial_number=serial_number)
        sender_panel = SenderPanel.objects.get(senders=sender)
        self.assertEqual(sender_panel.name, 'CD3/CD8/CD45/CD4 TRUC')
        utestids = [i.utestid.name for i in SenderPanelItem.objects.filter(
            sender_panel=sender_panel)]
        utestids.sort()
        self.assertEqual(utestids, ['CD4', 'CD4%', 'CD8', 'CD8%'])
        sender_utestids = [i.sender_utestid for i in SenderPanelItem.objects.filter(
            sender_panel=sender_panel)]
        sender_utestids.sort()
        self.assertEqual(sender_utestids, [
            '(Average) CD3+CD4+ Abs Cnt',
            '(Average) CD3+CD8+ %Lymph',
            '(Average) CD3+CD8+ Abs Cnt',
            'CD3/CD8/CD45/CD4 TruC CD3+CD4+ %Lymph']
        )
