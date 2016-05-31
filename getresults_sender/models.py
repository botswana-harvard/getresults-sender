from django.db import models

from simple_history.models import HistoricalRecords as AuditTrail
from edc_base.model.models import BaseUuidModel
from getresults_order.models import Utestid, OrderPanel


class SenderModel(BaseUuidModel):

    """A class for the model or make of a sending device, e.g. FACSCalibur."""

    name = models.CharField(
        max_length=25,
        unique=True
    )

    make = models.CharField(
        max_length=25,
        null=True,
    )

    description = models.CharField(
        max_length=100,
        null=True
    )

    history = AuditTrail()

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'getresults_sender'
        db_table = 'getresults_sendermodel'
        ordering = ('name', )


class Sender(BaseUuidModel):

    """A class for a specific sender device identified by serial number that links to a sender panel."""

    name = models.CharField(max_length=25, null=True, blank=True)

    sender_model = models.ForeignKey(SenderModel)

    serial_number = models.CharField(
        max_length=25,
        unique=True
    )

    def __str__(self):
        return '{} {}'.format(self.name, self.serial_number)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.serial_number
        super(Sender, self).save(*args, **kwargs)

    class Meta:
        app_label = 'getresults_sender'
        db_table = 'getresults_sender'
        ordering = ('serial_number', )


class SenderPanel(BaseUuidModel):

    """A class for the panel of results associated with a sending model/make."""

    name = models.CharField(max_length=25, unique=True)

    order_panel = models.ForeignKey(
        OrderPanel,
        null=True,
        help_text='Order panels linked to this sender panel')

    senders = models.ManyToManyField(
        Sender,
        help_text='senders that use this sender panel.')

    history = AuditTrail()

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'getresults_sender'
        db_table = 'getresults_senderpanel'
        ordering = ('name', )


class SenderPanelItem(BaseUuidModel):

    """A class for each result item in a sending device's panel linking the
    field name from the device to a utestid."""

    sender_panel = models.ForeignKey(SenderPanel)

    utestid = models.ForeignKey(
        to=Utestid,
        help_text='order utestid')

    sender_utestid = models.CharField(max_length=25)

    history = AuditTrail()

    def str(self):
        return '{} <--> {}'.format(self.sender_panel.name, self.utestid.name)

    class Meta:
        app_label = 'getresults_sender'
        db_table = 'getresults_senderpanelitem'
        unique_together = ('sender_panel', 'utestid')
