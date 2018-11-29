
from passlib.hash import sha256_crypt

# local imports
from .database import Database


class User(Database):

    __table__ = 'users'

    def save(self, **kwargs):
        if 'role_id' not in kwargs:
            kwargs['role_id'] = '1'
        kwargs['password'] = self.hash_password(kwargs.get('password'))
        return self.insert(self.__table__, kwargs)

    def query_user(self, **user_data):
        user = self.select(self.__table__, user_data)
        if user:
            user = user[0]
        return user

    @classmethod
    def hash_password(self, password):
        return sha256_crypt.encrypt(password)

    @classmethod
    def verify_password(self, password, input_password):
        return sha256_crypt.verify(input_password, password)
