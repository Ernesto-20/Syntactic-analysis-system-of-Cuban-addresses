from src.neural_networks.neural_parser import NeuralParser
from src.tools.decoder import Decoder


class AddressParser:

    def __init__(self, model: NeuralParser, decoder: Decoder):
        self.model = model
        self.decoder = decoder

    def process_address(self, address_list: list):
        probability_matrix = self.model.predict(address_list)

        return self.decoder.decoder_to_first_address_model(probability_matrix, address_list)
