from parser.tools.address_cleaner import AddressCleaner
from parser.neural_networks.lstm_cnn_model import LstmCnnModel
from noise_generator.tools.data_set_manage import DataSetManage


print('Loading Datasets')
eq1_data = DataSetManage.load( '../assets/default_data_set/model_type_three/EQ_S3_1000')

print('Creating Neural Model')

model = LstmCnnModel(eq1_data, AddressCleaner.cleaner_method('custom_standardization'),config=None,model=None)

