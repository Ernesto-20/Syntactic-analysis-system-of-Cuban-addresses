import pandas as pd

from data_preprocessing.address_cleaner import AddressCleaner
from neural_networks.deep_parser_model import DeepParserModel, DeepParserConfig
from src.tools.data_set_manage import DataSetManage


print('Loading Datasets')
eq1_data = DataSetManage.load( '../assets/default_data_set/model_type_two/EQ_S2_1000')

print('Creating Neural Model')

config = DeepParserConfig(
                output_emb_char=25,
                output_emb_trigram=25,
                output_emb_word=100,
                units_char_blstm=50,
                units_trigram_blstm=50,
                dropout_char_blstm=0.6,
                dropout_trigram_blstm=0.6,
                rdropout_char_blstm=0.1,
                rdropout_trigram_blstm=0.1,
                dropout_char_trigram_blstm=0.2,
                rdropout_char_trigram_blstm=0.1,
                dropout_char_trigram_word_blstm=0,
                rdropout_char_trigram_word_blstm=0,
            )

model = DeepParserModel(eq1_data, AddressCleaner.cleaner_method('custom_standardization'),config=config,model=None)

