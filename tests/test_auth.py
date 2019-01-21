
def test_user_signup(client, test_user):  # noqa F811
    response = client.post(
        '/api/v1/auth/signup',
        data=test_user, headers={'content-type': 'application/json'})
    assert response.status_code == 201
    assert b"user created successfully" in response.data


def test_user_login_wrong_password(client, wrong_user_details):
    response = client.post(
        '/api/v1/auth/login',
        data=wrong_user_details, headers={'content-type': 'application/json'})
    assert b"Invalid username or password" in response.data


def test_user_login(client, test_user_login):
    response = client.post(
        '/api/v1/auth/login',
        data=test_user_login, headers={'content-type': 'application/json'})
    assert b"Login success" in response.data
