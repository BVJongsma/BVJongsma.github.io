import mesa


class EnvelopeAgent(mesa.Agent):
    """The case file envelope containing the murder weapon and killer cards."""

    def __init__(self, unique_id, envelope_cards, model):
        super().__init__(unique_id, model)
        self.envelope_cards = envelope_cards

    # Get the cards that are in the envelope
    def get_envelope_cards(self):
        return self.envelope_cards