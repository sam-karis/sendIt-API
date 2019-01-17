
import click
from flask.cli import with_appcontext

from api.models.users import User
from api.models.roles import Role
from api.helpers.validators import validate_email

user = User()
role = Role()


@click.command()
@click.option('--name', prompt='Enter Admin full name', help='Admin Full names.')  # noqa E501
@click.option('--username', prompt='Enter Admin username', help='Admin username.')  # noqa E501
@click.option('--email', prompt='Enter Admin email', help='Admin email.')  # noqa E501
@click.password_option('--password', prompt='Enter Admin password', help='Admin password more than 6 characters.')  # noqa E501
@with_appcontext
def create_admin(name, username, email, password):
    filter_role = {'role': 'admin'}
    filter_user = {'username': username}
    admin_role = role.query_role(**filter_role)

    if not validate_email(email) or len(password) < 6:
        click.echo("Invalid email and password.")
        exit()
    person = user.query_user(**filter_user)
    if person:
        click.echo("User with that username exist")
        exit()

    admin_data = {
        'name': name,
        'username': username,
        'email': email,
        'password': password,
        'role_id': str(admin_role['id'])
    }

    user.save(**admin_data)

    click.echo("Admin added successfully")


if __name__ == '__main__':
    create_admin()
