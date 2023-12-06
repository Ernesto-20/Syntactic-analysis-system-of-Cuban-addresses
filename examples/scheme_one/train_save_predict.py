from src.parser.tools.neural_parser_manage import NeuralParserManage
from src.parser.neural_networks.deep_parser_model import DeepParserModel, DeepParserConfig
from src.parser.tools.address_cleaner import AddressCleaner
from src.noise_generator.tools.data_set_manage import DataSetManage

print('Init')

# Load dataset saved
data_set = DataSetManage.load('../../assets/default_data_set/model_type_one/DataSet_190000')

# Create configuration
config = DeepParserConfig(
    # Dimentions and units
    output_emb_char=  25,
    output_emb_trigram=25,
    output_emb_word= 100,
    units_char_blstm=256,
    units_trigram_blstm=256,
    units_word_blstm=512,
    # Dropouts
    dropout_char_blstm=0,
    dropout_trigram_blstm=0,
    rdropout_char_blstm=0,
    rdropout_trigram_blstm=0,
    dropout_char_trigram_blstm=0.1,
    rdropout_char_trigram_blstm=0,
    dropout_char_trigram_word_blstm=0.1,
    rdropout_char_trigram_word_blstm=0,
    # Other params
    learning_rate=0.0005
)

# Create model
model = DeepParserModel(data_set, AddressCleaner.cleaner_method('custom_standardization'))

# Train model
history = model.train(batch_size=560, epochs=10)

# Save model
NeuralParserManage.save_neural_parser(model, route='../assets/trained_models/model_type_one', name='pc_trained_v1')

# print(data_set.get_id_to_category())
# print(data_set.get_n_tag())
# parser = AddressParser(model, Decoder(data_set.get_id_to_category(),
#                                               AddressCleaner.cleaner_method('custom_standardization')))
# parser.process_address(['Hola compadre'])
#
# # save
# NeuralParserManage.save_neural_parser(model, route='../assets/trained_models/model_type_one', name='pc_trained_v1')
# import matplotlib.pyplot as plt
#
# print(history.history.keys())
# acc = history.history['categorical_accuracy']
# val_acc = history.history['val_categorical_accuracy']
# loss = history.history['loss']
# val_loss = history.history['val_loss']
#
# epochs = 1
# plt.plot(epochs, acc, 'bo', label='Training acc')
# plt.plot(epochs, val_acc, 'b', label='Validation acc')
# plt.title('Training and validation accuracy')
# plt.legend()
# plt.figure()
# plt.plot(epochs, loss, 'bo', label='Training loss')
# plt.plot(epochs, val_loss, 'b', label='Validation loss')
# plt.title('Training and validation loss')
# plt.legend()
# plt.show()
print('Finish')
