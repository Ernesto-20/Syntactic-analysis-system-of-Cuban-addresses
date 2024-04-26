from noise_generator.tools.data_set_manage import DataSetManage
from parser.neural_networks.deep_parser_model import DeepParserConfig, DeepParserModel
from parser.tools.address_cleaner import AddressCleaner
from parser.tools.neural_parser_manage import NeuralParserManage

# load dataset saved
tp = 'eq'
address = 100

data_set = DataSetManage.load(f'../../assets/default_data_set/model_type_three/{tp}_S3_{address}')

config = DeepParserConfig(
    # Dimentions and units
    output_emb_char=256,
    output_emb_trigram=256,
    output_emb_word=128,
    units_char_blstm=64,
    units_trigram_blstm=64,
    units_word_blstm=64,
    # Dropouts
    dropout_char_blstm=0.2,
    dropout_trigram_blstm=0.2,
    rdropout_char_blstm=0.1,
    rdropout_trigram_blstm=0.1,
    dropout_char_trigram_blstm=0.3,
    rdropout_char_trigram_blstm=0.1,
    dropout_char_trigram_word_blstm=0.4,
    rdropout_char_trigram_word_blstm=0.2,
    # Other params
    learning_rate=0.001,
)

model = DeepParserModel(data_set, AddressCleaner.cleaner_method('custom_standardization_v2'), config=config)

print('Training')
# train
epochs = 1
history = model.train(batch_size=100, epochs=epochs)

# save
NeuralParserManage.save_neural_parser(model, route='../../assets/trained_models/model_type_three',
                                      name='modelo_prueba')
print('Finish')