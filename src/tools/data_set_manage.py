import pickle

from src.tools.address_data_set import DataSet


class DataSetManage:
    @staticmethod
    def save(data_set: DataSet, route_and_name: str):
        if type(route_and_name) is not str:
            raise NotImplementedError('route variable could be string instance')
        with open(route_and_name + '.pickle', "wb") as file:
            pickle.dump(data_set, file)

    @staticmethod
    def load(route_and_name) -> DataSet:
        data_set = None
        with open(route_and_name + '.pickle', "rb") as file:
            data_set = pickle.load(file)

        if  type(route_and_name) is None:
            raise NotImplementedError('route and name data set is not found')

        return data_set

    def export_data(sefl,df, filename, file_format='csv'):
        if file_format == 'csv':
            df.to_csv(filename + '.csv', index=False)
        elif file_format == 'xlsx':
            df.to_excel(filename + '.xlsx', index=False)