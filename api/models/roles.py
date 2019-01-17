
# local imports
from .database import Database


class Role(Database):

    __table__ = 'roles'

    def query_role(self, **role_id):
        role = self.select(self.__table__, role_id)
        if role:
            role = role[0]
        return role
