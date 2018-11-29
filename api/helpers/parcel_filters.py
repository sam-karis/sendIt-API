
from api.models.parcels import Parcel
from api.helpers.validators import validate_id

parcel = Parcel()


def get_parcel_to_edit(parcel_id, filter_data):
    validate_id('parcel id', parcel_id)
    parcel_to_edit = parcel.query_parcel(**filter_data)
    return parcel_to_edit
