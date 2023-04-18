# Encontré como descargar el dataset original del articulo DeepParse

import pandas as pd
import tensorflow_datasets as tfds
from datasets import load

ds_english = load.load_dataset('conll2003')
print("Dataset cargado")
print(ds_english.shape)
print(ds_english.column_names)


conll2003_train = pd.DataFrame(ds_english['train'])
conll2003_validation = pd.DataFrame(ds_english['validation'])
conll2003_test = pd.DataFrame(ds_english['test'])

conll2003_train.to_excel('conll2003_train.xlsx', index=False)
conll2003_validation.to_excel('conll2003_validation.xlsx', index=False)
conll2003_test.to_excel('conll2003_test.xlsx', index=False)
print("Dataset exportado a excel")
