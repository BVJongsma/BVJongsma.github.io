import mesa


class EnvelopeAgent(mesa.Agent):
    """The envelope containing the murder weapon and killer cards."""

    def __init__(self, unique_id, envelope_cards, model):
        super().__init__(unique_id, model)
        self.envelope_cards = envelope_cards