import csv
import os

from django.conf import settings
from getresults_order.models import Utestid, OrderPanel

from .models import SenderPanel, SenderPanelItem, SenderModel, Sender


class SenderMetaData(object):
    """A class to import from CSV meta data into SenderPanel, SenderPanelItem,
    SenderModel, Sender, Utestid, OrderPanel.

    Any sender name referred to in the Sender Panel file must exist in the Sender file
    or the sender model"""

    def __init__(self, sender_panel_file=None, sender_file=None):
        self.sender_panel_file = (sender_panel_file or
                                  os.path.join(settings.BASE_DIR, 'testdata/sender_panels.csv'))
        self.sender_file = sender_file or os.path.join(settings.BASE_DIR, 'testdata/senders.csv')
        self.load_senders_from_csv()
        self.load_sender_panels_from_csv()

    def load_sender_panels_from_csv(self):
        """sender_model,utestid,sender_field_name,sender_panel"""
        with open(self.sender_panel_file, 'r') as f:
            reader = csv.reader(f, quotechar="'")
            header = next(reader)
            header = [h.lower() for h in header]
            for row in reader:
                r = dict(zip(header, row))
                sender_panel = self.sender_panel(
                    sender_panel_name=r['sender_panel'].strip(),
                    order_panel_name=r['order_panel'].strip(),
                    sender_serial_number=r['sender_serial_number'].strip())
                utestid = Utestid.objects.get(name=r['utestid'].strip())
                sender_utestid = r['sender_utestid'].strip()
                try:
                    SenderPanelItem.objects.get(
                        sender_panel=sender_panel,
                        utestid=utestid,
                        sender_utestid=sender_utestid)
                except SenderPanelItem.DoesNotExist:
                    SenderPanelItem.objects.create(
                        sender_panel=sender_panel,
                        utestid=utestid,
                        sender_utestid=sender_utestid)

    def load_senders_from_csv(self):
        with open(self.sender_file, 'r') as f:
            reader = csv.reader(f, quotechar="'")
            header = next(reader)
            header = [h.lower() for h in header]
            for row in reader:
                r = dict(zip(header, row))
                self.sender(
                    sender_serial_number=r['serial_number'].strip(),
                    sender_model_name=r['sender_model'].strip())

    def sender_model(self, name):
        try:
            sender_model = SenderModel.objects.get(name=name)
        except SenderModel.DoesNotExist:
            sender_model = SenderModel.objects.create(name=name)
        return sender_model

    def sender(self, sender_serial_number, sender_model_name=None):
        try:
            sender = Sender.objects.get(serial_number=sender_serial_number)
        except Sender.DoesNotExist:
            sender = Sender.objects.create(
                name=sender_serial_number,
                serial_number=sender_serial_number,
                sender_model=self.sender_model(name=sender_model_name))
        return sender

    def order_panel(self, name):
        try:
            order_panel = OrderPanel.objects.get(name=name)
        except OrderPanel.DoesNotExist:
            order_panel = OrderPanel.objects.create(name=name)
        return order_panel

    def sender_panel(self, sender_panel_name, order_panel_name, sender_serial_number):
        try:
            sender_panel = SenderPanel.objects.get(
                name=sender_panel_name)
        except SenderPanel.DoesNotExist:
            sender_panel = SenderPanel.objects.create(
                name=sender_panel_name,
                order_panel=self.order_panel(order_panel_name))
        sender_panel.senders.add(self.sender(sender_serial_number))
        return sender_panel
