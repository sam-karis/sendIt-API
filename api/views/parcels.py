
from flask_restplus import Resource
from flask import jsonify, request
from flask_jwt_extended import (jwt_required)

# local imports
from api.helpers.schema.parcel import (
    CreateSchema, DestinationSchema, StatusSchema, PresentLocationSchema)
from api.models.parcels import Parcel
from api.helpers.auth import (get_user_identity, admin_required)
from api.helpers.validators import validate_id
from api.helpers.parcel_filters import get_parcel_to_edit


parcel = Parcel()


class CreateGetParcelsResource(Resource):

    @jwt_required
    def post(self):
        '''Create parcel'''
        current_user = get_user_identity()
        request_data = request.get_json()
        new_parcel_data = CreateSchema().load_json_data(request_data)
        new_parcel_data['user_id'] = str(current_user['id'])
        parcel_created = parcel.save(**new_parcel_data)

        response = jsonify({
            'message': 'parcel created successfully',
            'parcel': parcel_created
        })
        response.status_code = 201
        return response

    @jwt_required
    @admin_required
    def get(self):
        '''Get all parcels by admin'''
        parcels = parcel.query_all_parcel()
        response = jsonify({
             'message': f"A total of {len(parcels)} parcels ordered.",
             'parcels': parcels})
        return response


class GetParcelByIdResource(Resource):

    @jwt_required
    @admin_required
    def get(self, parcelId):
        '''Get parcel by id'''
        validate_id('parcel id', parcelId)
        parcel_id = {'id': str(parcelId)}
        parcel_from_db = parcel.query_parcel(**parcel_id)
        if not parcel_from_db:
            return jsonify({"message": f"No parcel with id {parcelId}"})
        return jsonify(parcel_from_db)


class GetUserParcelsResource(Resource):

    @jwt_required
    def get(self, userId, parcelId=None):
        '''Get users parcel by id'''
        current_user = get_user_identity()
        validate_id('user id', userId, current_user)
        filter_data = {'user_id': userId}
        res = 'parcels'
        if parcelId:
            res = f'parcel id {parcelId}'
            validate_id('parcel id', parcelId)
            filter_data['id'] = parcelId
        parcels = parcel.query_parcel(**filter_data)
        if not parcels:
            response = jsonify(
                {"message": f"{current_user['username']} has no {res} ordered."})  # noqa E501
            response.status_code = 404
            return response
        return jsonify({
            'message': f"{current_user['username']} has ordered {len(parcels)} parcels",  # noqa E501
            'parcels': parcels
        })


class CancelParcelResource(Resource):

    @jwt_required
    def put(self, parcelId):
        current_user = get_user_identity()
        filter_data = {'user_id': str(current_user['id']), 'id': str(parcelId)}
        parcel_to_cancel = get_parcel_to_edit(parcelId, filter_data)
        if parcel_to_cancel:
            new_parcel_data = {'status': 'cancel'}
            editted_parcel = parcel.update_parcel(parcelId, **new_parcel_data)
            return jsonify(editted_parcel)
        return jsonify({"message": f"{current_user['username']} has no parcel of id {parcelId}."})  # noqa E501


class EditParcelDestinationResource(Resource):

    @jwt_required
    def put(self, parcelId):
        current_user = get_user_identity()
        filter_data = {'user_id': str(current_user['id']), 'id': str(parcelId)}
        parcel_to_edit = get_parcel_to_edit(parcelId, filter_data)
        if parcel_to_edit:
            request_data = request.get_json()
            new_parcel_data = DestinationSchema().load_json_data(request_data)
            editted_parcel = parcel.update_parcel(parcelId, **new_parcel_data)
            return jsonify({
                'message': 'Destination changed successfully',
                'parcel': editted_parcel})
        return jsonify({"message": f"{current_user['username']} has no parcel of id {parcelId}."})  # noqa E501


class EditParcelStatusResource(Resource):

    @jwt_required
    @admin_required
    def put(self, parcelId):
        filter_data = {'id': str(parcelId)}
        parcel_to_edit = get_parcel_to_edit(parcelId, filter_data)
        if parcel_to_edit:
            request_data = request.get_json()
            new_parcel_data = StatusSchema().load_json_data(request_data)
            editted_parcel = parcel.update_parcel(parcelId, **new_parcel_data)
            return jsonify(editted_parcel)
        return jsonify({"message": f"No parcel id {parcelId}."})


class EditParcelPresentLocationResource(Resource):

    @jwt_required
    @admin_required
    def put(self, parcelId):
        filter_data = {'id': str(parcelId)}
        parcel_to_edit = get_parcel_to_edit(parcelId, filter_data)
        if parcel_to_edit:
            request_data = request.get_json()
            new_parcel_data = PresentLocationSchema().load_json_data(request_data)  # noqa E501
            editted_parcel = parcel.update_parcel(parcelId, **new_parcel_data)
            return jsonify(editted_parcel)
        return jsonify({"message": f"No parcel id {parcelId}."})
