
import os
import psycopg2
import psycopg2.extras
from psycopg2.extras import RealDictCursor
from flask_json import JsonError
from urllib.parse import urlparse

from config import config


class Database():

    def __init__(self):
        # Get database uri from config
        config_env = os.getenv('FLASK_ENV', default='development')
        DATABASE_URI = config[config_env].DATABASE_URI
        db_uri = urlparse(DATABASE_URI)
        # Create a db connection
        self.connection = psycopg2.connect(
            database=db_uri.path[1:],
            user=db_uri.username,
            host=db_uri.hostname,
            password=db_uri.password
        )
        # create a cursor
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

    def excute_query(self, table_query):
        try:
            self.cursor.execute(table_query)
            self.connection.commit()
            return self.cursor
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            if 'duplicate key value violates unique constraint' in str(error):
                raise JsonError(
                    error='User with that username or email already exists.')
            raise JsonError(error=str(error))

    def insert(self, target_table, data):
        table_columns = ", ".join(data.keys())
        column_values = "', '".join(data.values())

        INSERT_QUERY = (
            f"INSERT INTO {target_table} (id, {table_columns})\
            VALUES (DEFAULT, '{column_values}')\
            RETURNING id, {table_columns};"
        )
        cursor = self.excute_query(INSERT_QUERY)

        return cursor.fetchone()

    def select(self, target_table, filter_data=None):
        filter_by = ''
        if filter_data:
            columns_values = ''
            for key, value in filter_data.items():
                columns_values += f"{key}='{value}' AND "
            columns_values = columns_values.strip(' AND ')
            filter_by = f"WHERE {columns_values}"
        SELECT_QUERY = f"SELECT * FROM {target_table} {filter_by};"
        cursor = self.excute_query(SELECT_QUERY)
        return cursor.fetchall()

    def update(self, target_table, id, update_data, return_data=('id')):
        columns_values = ''
        return_data = ", ".join(return_data)
        if update_data:
            for key, value in update_data.items():
                columns_values += f"{key} = '{value}',"
        columns_values = columns_values.strip(',')

        UPDATE_QUERY = (
            f"UPDATE {target_table}\
            SET {columns_values}\
            WHERE id='{id}'\
            RETURNING {return_data}"
        )
        cursor = self.excute_query(UPDATE_QUERY)
        return cursor.fetchone()


class Migrate(Database):

    def create_tables(self):
        CREATE_TABLES_QUERY = (
            """
            CREATE TABLE IF NOT EXISTS roles (
                id serial PRIMARY KEY NOT NULL,
                role VARCHAR(60) NOT NULL UNIQUE DEFAULT 'default_user'
                );

            INSERT INTO roles (role) SELECT 'default_user' WHERE NOT EXISTS (
                SELECT * FROM roles where role='default_user');
            INSERT INTO roles (role) SELECT 'admin' WHERE NOT EXISTS (
                SELECT * FROM roles where role='admin');

            CREATE TABLE IF NOT EXISTS users (
                id serial PRIMARY KEY NOT NULL,
                role_id integer NOT NULL,
                name VARCHAR(60) NOT NULL,
                username VARCHAR(60) UNIQUE NOT NULL,
                email VARCHAR(60) UNIQUE NOT NULL,
                password VARCHAR(250) NOT NULL,
                FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
                );

            CREATE TABLE IF NOT EXISTS parcels (
                id serial PRIMARY KEY NOT NULL,
                user_id integer NOT NULL,
                title VARCHAR(60) NOT NULL,
                destination VARCHAR(60) NOT NULL,
                current_location VARCHAR(60) NOT NULL DEFAULT '',
                quantity VARCHAR(60) NOT NULL,
                status VARCHAR(60) NOT NULL DEFAULT 'pending',
                date_ordered timestamp DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );
            """
        )

        self.excute_query(CREATE_TABLES_QUERY)

    def drop_tables(self):
        DROP_TABLES_QUERY = (
            """
            DROP TABLE IF EXISTS roles CASCADE;
            DROP TABLE IF EXISTS users CASCADE;
            DROP TABLE IF EXISTS parcels CASCADE;
            """
        )
        self.excute_query(DROP_TABLES_QUERY)
