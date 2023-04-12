from abc import ABC, abstractmethod

from src.tools.address_cleaner import AddressCleaner
from src.tools.address_data_set import DataSet

import tensorflow as tf


class NeuralParser(ABC):

    @abstractmethod
    def predict(self, address_list: list):
        pass

    @abstractmethod
    def train(self, batch_size=1200, epochs=50):
        pass

    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def get_address_cleaner(self) -> AddressCleaner:
        pass

    @abstractmethod
    def get_data(self) -> DataSet:
        pass

    @abstractmethod
    def get_model(self) -> tf.keras.Model:
        pass