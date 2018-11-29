
# local imports
from .database import Database


class Parcel(Database):

    __table__ = 'parcels'
    return_columns = ('id', 'title', 'destination',
                      'current_location', 'quantity', 'status', 'date_ordered')

    def save(self, **kwargs):
        return self.insert(self.__table__, kwargs)

    def query_parcel(self, **parcel_data):
        return self.select(self.__table__, parcel_data)

    def query_all_parcel(self):
        return self.select(self.__table__)

    def update_parcel(self, id, **kwargs):
        return self.update(self.__table__, id, kwargs, self.return_columns)
