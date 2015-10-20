import csv
import os

from django.conf import settings
from getresults_order.models import Utestid, OrderPanel

from .models import SenderPanel, SenderPanelItem, SenderModel, Sender


def load_sender_panels_from_csv(csv_filename=None):
    """sender_model,utestid,sender_field_name,sender_panel"""
    csv_filename = csv_filename or os.path.join(settings.BASE_DIR, 'testdata/sender_panels.csv')
    with open(csv_filename, 'r') as f:
        reader = csv.reader(f, quotechar="'")
        header = next(reader)
        header = [h.lower() for h in header]
        for row in reader:
            r = dict(zip(header, row))
            try:
                sender_model = SenderModel.objects.get(name=r['sender_serial_number'].strip())
            except SenderModel.DoesNotExist:
                sender_model = SenderModel.objects.create(name=r['sender_serial_number'].strip())
            try:
                sender = Sender.objects.get(serial_number=r['sender_serial_number'])
            except Sender.DoesNotExist:
                sender = Sender.objects.create(
                    name=r['sender_serial_number'],
                    serial_number=r['sender_serial_number'],
                    sender_model=sender_model)
            try:
                order_panel = OrderPanel.objects.get(name=r['order_panel'])
            except OrderPanel.DoesNotExist:
                order_panel = OrderPanel.objects.create(name=r['order_panel'])
            try:
                sender_panel = SenderPanel.objects.get(
                    name=r['sender_panel'].strip())
            except SenderPanel.DoesNotExist:
                sender_panel = SenderPanel.objects.create(
                    name=r['sender_panel'].strip(),
                    order_panel=order_panel)
            sender_panel.senders.add(sender)
            utestid = Utestid.objects.get(name=r['utestid'].strip())
            sender_utestid = r['sender_utestid'].strip()
            try:
                SenderPanelItem.objects.get(
                    sender_panel=sender_panel,
                    utestid=utestid,
                    sender_utestid=sender_utestid,)
            except SenderPanelItem.DoesNotExist:
                SenderPanelItem.objects.create(
                    sender_panel=sender_panel,
                    utestid=utestid,
                    sender_utestid=sender_utestid)


def load_senders_from_csv(csv_filename=None):
    csv_filename = csv_filename or os.path.join(settings.BASE_DIR, 'testdata/senders.csv')
    with open(csv_filename, 'r') as f:
        reader = csv.reader(f, quotechar="'")
        header = next(reader)
        header = [h.lower() for h in header]
        for row in reader:
            r = dict(zip(header, row))
            serial_number = r['serial_number'].strip()
            try:
                Sender.objects.get(serial_number=serial_number)
            except Sender.DoesNotExist:
                try:
                    sender_model = SenderModel.objects.get(name=r['sender_model'].strip())
                except SenderModel.DoesNotExist:
                    sender_model = SenderModel.objects.create(name=r['sender_model'].strip())
                Sender.objects.create(
                    name=serial_number,
                    serial_number=serial_number,
                    sender_model=sender_model)
