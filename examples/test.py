from src.data_preprocessing.address_cleaner import AddressCleaner

fuc = AddressCleaner.cleaner_method('custom_standardization')

print(fuc)
print('type: ', type(fuc))
