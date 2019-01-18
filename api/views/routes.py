
from api import api
from .users import RegisterUserResource, LoginUserResource
from .parcels import (CreateGetParcelsResource, CancelParcelResource,
                      GetUserParcelsResource, EditParcelDestinationResource,
                      GetParcelByIdResource, EditParcelStatusResource,
                      EditParcelPresentLocationResource)

# users urls
api.add_resource(RegisterUserResource, '/auth/signup')
api.add_resource(LoginUserResource, '/auth/login')
# Parcels urls
api.add_resource(CreateGetParcelsResource, '/parcels')
api.add_resource(GetParcelByIdResource, '/parcels/<parcelId>')
api.add_resource(CancelParcelResource, '/parcels/<parcelId>/cancel')
api.add_resource(EditParcelDestinationResource, '/parcels/<parcelId>/destination')  # noqa E501
api.add_resource(EditParcelStatusResource, '/parcels/<parcelId>/status')
api.add_resource(EditParcelPresentLocationResource, '/parcels/<parcelId>/presentLocation')  # noqa E501

# user parcels urls
api.add_resource(GetUserParcelsResource, '/users/<userId>/parcels/')
api.add_resource(GetUserParcelsResource, '/users/<userId>/parcels/<parcelId>')
