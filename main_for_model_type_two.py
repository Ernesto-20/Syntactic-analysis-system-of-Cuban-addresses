# import string
import pandas as pd

from src.data_realism_converter.data_set_adapter import DataSetAdapter
from src.data_realism_converter.noise_generator import NoiseGenerator
from src.neural_networks.deep_parser_model import DeepParserModel

print('Init')
data = pd.read_excel('assets/default_corpus/model_type_one/corpus_1.xlsx')

generator = NoiseGenerator()
data_with_noise = generator.generate_noise(data, address_amount=8000)

# Especificar en la clase adapter los parametros de conjunto de datos para el entrenamiento, prueba y validación
adapt = DataSetAdapter()
data_set = adapt.adapt_data_set(data_with_noise)

# Eliminar el metodo create_model y asignarlo al constructor.
parser = DeepParserModel()
parser.create_model(data_set)
parser.fit_model(data_set, batch_size=500, epochs=15)
# parser.save_model('DeepParser_1000_address')
result = parser.predict(['calle parque entre av. carolina, san miguel del padron', 'vista hermosa, San miguel del padro, e/ ave. carolina y cale garido.',
                         'vista hermosa, San miguel del padro, e/ ave. carolina y cale garido reparto vista hermosa'])


print('finish')