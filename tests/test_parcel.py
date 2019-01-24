
def test_create_parcel(client, parcel, access_token):
    response = client.post(
        '/api/v1/parcels', data=parcel, headers={
            'content-type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        })
    assert response.status_code == 201
    assert b"parcel created successfully" in response.data


def test_update_parcel_destination(client, access_token, new_destination):
    response = client.put(
        '/api/v1/parcels/1/destination', data=new_destination, headers={
            'content-type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        })
    assert b'Destination changed successfully' in response.data


def test_get_user_parcels(client, access_token):
    response = client.get(
        '/api/v1/users/1/parcels', headers={
            'content-type': 'application/json',
            'Authorization': f'Bearer {access_token}'
            })
    assert b"test has ordered 1 parcels" in response.data


def test_get_user_parcels_by_id(client, access_token):
    response = client.get(
        '/api/v1/users/1/parcels/1', headers={
            'content-type': 'application/json',
            'Authorization': f'Bearer {access_token}'
            })
    assert b"test has ordered 1 parcels" in response.data
    assert b"laptop" in response.data


def test_get_user_parcels_by_invalid_id(client, access_token):
    response = client.get(
        '/api/v1/users/1/parcels/100', headers={
            'content-type': 'application/json',
            'Authorization': f'Bearer {access_token}'
            })
    assert b"test has no parcel id 100 ordered." in response.data
