from abc import ABC, abstractmethod
from typing import Callable

from noise_generator.address_data_set import DataSet
import tensorflow as tf
import numpy as np


class NeuralParser(ABC):

    def predict(self, address_list: list):
        print(self.data.get_id_to_category())
        result = self.model.predict(address_list)

        return np.round(result, decimals=4)

    def train(self, batch_size=1200, epochs=50):
        # tensorboard_callback = keras.callbacks.TensorBoard(
        #     log_dir='tb_callback_dir', histogram_freq=0
        # )

        x = np.asarray(self.data.get_x_train_values())
        y = self.data.get_y_train_values()
        x_val = np.asarray(self.data.get_x_val_values())
        y_val = self.data.get_y_val_values()
        history = self.model.fit(x, y,
                                 batch_size=batch_size,
                                 verbose=1,
                                 epochs=epochs,
                                 validation_data=(x_val, y_val),
                                 # callbacks=[tensorboard_callback]
                                 )

        return history

    def evaluate(self):
        history = self.model.evaluate(
            np.asarray(self.data.get_x_test_values()),
            self.data.get_y_test_values())

        return history

    @property
    @abstractmethod
    def cleaner_method(self) -> Callable:
        pass

    @property
    @abstractmethod
    def data(self) -> DataSet:
        pass

    @property
    @abstractmethod
    def model(self) -> tf.keras.Model:
        pass

    @property
    @abstractmethod
    def config(self):
        pass
