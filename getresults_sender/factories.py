import factory

from getresults_sender.models import SenderModel, SenderPanel, Sender


class SenderModelFactory(factory.DjangoModelFactory):

    class Meta:
        model = SenderModel

    name = factory.Sequence(lambda n: 'sendermodel{}'.format(n))


class SenderFactory(factory.DjangoModelFactory):

    class Meta:
        model = Sender

    name = factory.Sequence(lambda n: 'sender{}'.format(n))

    serial_number = factory.Sequence(lambda n: 'sn{}'.format(str(n).zfill(7)))

    sender_model = factory.SubFactory(SenderModelFactory)


class SenderPanelFactory(factory.DjangoModelFactory):

    """ SenderPanelFactory.create(senders=(sender1, sender2, sender3))"""

    class Meta:
        model = SenderPanel

    name = factory.Sequence(lambda n: 'senderpanel{}'.format(n))

    @factory.post_generation
    def senders(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for sender in extracted:
                self.senders.add(sender)
