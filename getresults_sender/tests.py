from django.test import TestCase
from getresults_order.utils import load_utestids_from_csv

from .models import Sender, SenderPanelItem, SenderPanel
from .sender_meta_data import SenderMetaData
from getresults_order.utils.load_order_panels_from_csv import load_order_panels_from_csv


class TestGetresults(TestCase):

    def setUp(self):
        load_utestids_from_csv()
        load_order_panels_from_csv()
        sender_meta_data = SenderMetaData()
        sender_meta_data.load_all()

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
