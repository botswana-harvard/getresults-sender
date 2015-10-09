from django.db import models

from edc_base.model.models import BaseUuidModel, HistoricalRecords
from getresults_order.models import Utestid


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

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'getresults_order'
        db_table = 'getresults_sendermodel'
        ordering = ('name', )


class SenderPanel(BaseUuidModel):

    """A class for the panel of results associated with a sending model/make."""

    name = models.CharField(max_length=25, unique=True)

    sender_model = models.ForeignKey(SenderModel)

    history = HistoricalRecords()

    def __str__(self):
        return '{}: {}'.format(self.sender_model.name, self.name)

    class Meta:
        app_label = 'getresults_order'
        db_table = 'getresults_senderpanel'
        ordering = ('name', )
        unique_together = ('sender_model', 'name')


class SenderPanelItem(BaseUuidModel):

    """A class for each item in a sending device's panel linking the field name from the device to a utestid."""

    sender_panel = models.ForeignKey(SenderPanel)

    utestid = models.ForeignKey(Utestid)

    sender_utestid = models.CharField(max_length=25)

    history = HistoricalRecords()

    def str(self):
        return '{} <--> {}'.format(self.sender_panel.name, self.utestid.name)

    class Meta:
        app_label = 'getresults_order'
        db_table = 'getresults_senderpanelitem'
        unique_together = ('sender_panel', 'utestid')


class Sender(BaseUuidModel):

    """A class for a specific sender device identified by serial number that links to a sender panel."""

    sender_model = models.ForeignKey(SenderModel)

    serial_number = models.CharField(
        max_length=25,
        unique=True
    )

    sender_panel = models.ForeignKey(SenderPanel)

    class Meta:
        app_label = 'getresults_order'
        db_table = 'getresults_sender'
        ordering = ('serial_number', )
