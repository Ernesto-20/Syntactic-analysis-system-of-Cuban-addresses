import src.parser.neural_networks.deep_parser_model
config = src.parser.neural_networks.deep_parser_model.DeepParserConfig(
    # Dimentions and units
    output_emb_char=  256,
    output_emb_trigram=256,
    output_emb_word= 128,
    units_char_blstm=64,
    units_trigram_blstm=64,
    units_word_blstm=64,
    # Dropouts
    dropout_char_blstm=0,
    dropout_trigram_blstm=0,
    rdropout_char_blstm=0,
    rdropout_trigram_blstm=0,
    dropout_char_trigram_blstm=0.2,
    rdropout_char_trigram_blstm=0,
    dropout_char_trigram_word_blstm=0.3,
    rdropout_char_trigram_word_blstm=0,
    # Other params
    learning_rate=0.005
)
import dill

dill.dump(config, open('config', 'wb'))
print('finish')