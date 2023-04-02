import pickle

from src.utils.data_set import DataSet
import string


class ManageDataSet:
    def save(self, data_set: DataSet, route_and_name):
        if  type(route_and_name) is not str:
            raise NotImplementedError('route variable could be string instance')
        with open(route_and_name + '.pickle', "wb") as file:
            pickle.dump(data_set, file)

    def load(self, route_and_name):
        data_set = None
        with open(route_and_name + '.pickle', "rb") as file:
            data_set = pickle.load(file)

        if  type(route_and_name) is None:
            raise NotImplementedError('route and name data set is not found')

        return data_set
