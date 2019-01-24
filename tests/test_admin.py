
def test_get_all_parcels_by_user(client, parcel, access_token):
    # create dummy parcels
    for _ in range(5):
        client.post('/api/v1/parcels', data=parcel, headers={
                'content-type': 'application/json',
                'Authorization': f'Bearer {access_token}'})
    response = client.get(
        '/api/v1/parcels', headers={
            'content-type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        })
    assert b"You don't have access to this functionality." in response.data


def test_get_all_parcels_admin(client, parcel, admin_access_token):
    response = client.get(
        '/api/v1/parcels', headers={
            'content-type': 'application/json',
            'Authorization': f'Bearer {admin_access_token}'
        })
    assert b"A total of 5 parcels ordered." in response.data
    assert b"parcels" in response.data


def test_update_parcel_status(client, admin_access_token, new_status):
    response = client.put(
        '/api/v1/parcels/1/status', data=new_status,
        headers={
            'content-type': 'application/json',
            'Authorization': f'Bearer {admin_access_token}'
        })
    assert b"Parcel status editted successfully." in response.data


def test_update_parcel_location(client, admin_access_token, new_location):
    response = client.put(
        '/api/v1/parcels/1/presentLocation', data=new_location,
        headers={
            'content-type': 'application/json',
            'Authorization': f'Bearer {admin_access_token}'
        })
    assert b"Parcel location editted successfully." in response.data


def test_cancel_parcel_order(client, access_token):
    response = client.put(
        '/api/v1/parcels/1/cancel', headers={
            'content-type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        })
    assert b"Parcel cancelled successfully." in response.data
    # Test to cancel an order twice
    response = client.put(
        '/api/v1/parcels/1/cancel', headers={
            'content-type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        })
    assert b"Parcel already cancelled." in response.data
