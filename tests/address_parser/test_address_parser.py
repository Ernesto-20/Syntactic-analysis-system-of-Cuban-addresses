from src.address_parser.address_parser import AddressParser
from src.tools.decoder import Decoder
from src.tools.neural_parser_manage import NeuralParserManage
from src.structured_direction.classified_address_one import ClassifiedAddressOne

def test_parsing_address():
    neural_parser = NeuralParserManage.load_neural_parser(route='assets/trained_models/model_type_one', name='default_model_instance_1C')
    address_parser = AddressParser(neural_parser, Decoder(neural_parser.get_data().get_id_to_category(),
                                                          neural_parser.get_cleaner_method()))
    result = address_parser.process_address(['calle parque entre avenida carolina y calle garrido, reparto carolina, san miguel del padron, la habana'])[0]
    print('********')
    print(result)
    print('********')

    expected = ClassifiedAddressOne(principal_street=['parque'],
                                      first_side_street=['avenida', 'carolina'],
                                      second_side_street=['garrido'],
                                      locality=['carolina'],
                                      municipality=['san', 'miguel', 'del', 'padron'],
                                      province=['la', 'habana'],
                                      building=[],
                                      apartment=[],
                                      reserve_word=['calle', 'entre', 'y', 'calle', 'reparto', ',', ',', ','])

    if result == expected:
        print('they are equals')
    else:
        print('they are not equals')

    assert result == expected