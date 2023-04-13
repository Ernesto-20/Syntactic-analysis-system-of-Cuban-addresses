from keras.models import Sequential
from keras.layers import Embedding, Conv1D, Dropout, Bidirectional, LSTM, Concatenate
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from nltk.tokenize import word_tokenize
from nltk.util import ngrams

# Cargar los datos
datos = ["texto 1", "texto 2", "texto 3"]

# Crear la capa de tokenización de caracteres
tokenizer_char = Tokenizer(char_level=True)
tokenizer_char.fit_on_texts(datos)
sequences_char = tokenizer_char.texts_to_sequences(datos)
padded_sequences_char = pad_sequences(sequences_char)

# Crear la capa de tokenización de palabras
tokenizer_word = Tokenizer()
tokenizer_word.fit_on_texts(datos)
sequences_word = tokenizer_word.texts_to_sequences(datos)
padded_sequences_word = pad_sequences(sequences_word)

# Crear la capa de trigramas
trigrams = []
for text in datos:
    tokens = word_tokenize(text)
    trigrams.extend(list(ngrams(tokens, 3)))
tokenizer_trigram = Tokenizer()
tokenizer_trigram.fit_on_texts(trigrams)
sequences_trigram = tokenizer_trigram.texts_to_sequences(trigrams)
padded_sequences_trigram = pad_sequences(sequences_trigram)

# Unir las salidas con la capa Embedding y agregar una capa Bidirectional LSTM
embedding_dim = 100
input_dim_char = len(tokenizer_char.word_index) + 1
input_dim_word = len(tokenizer_word.word_index) + 1
input_dim_trigram = len(tokenizer_trigram.word_index) + 1

model = Sequential()
model.add(Embedding(input_dim_char, embedding_dim))
model.add(Bidirectional(LSTM(64)))
model.add(Embedding(input_dim_word, embedding_dim))
model.add(Bidirectional(LSTM(64)))
model.add(Embedding(input_dim_trigram, embedding_dim))
model.add(Bidirectional(LSTM(64)))

# Unir las salidas con la clase Concatenate y agregar la capa Conv1D y Dropout
concatenated_layer = Concatenate()([model.layers[1].output, model.layers[5].output])
conv_layer = Conv1D(filters=32, kernel_size=3, padding='same', activation='relu')(concatenated_layer)
dropout_layer = Dropout(0.5)(conv_layer)

# Compilar el modelo
model_final = Sequential()
model_final.add(model)
model_final.add(concatenated_layer)
model_final.add(conv_layer)
model_final.add(dropout_layer)

model_final.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])