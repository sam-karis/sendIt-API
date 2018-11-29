
from flask_restplus import Resource
from flask import jsonify, request, Response
from flask_jwt_extended import (jwt_required)

from app import api
from api.helpers.schema.parcel import (
    CreateSchema, DestinationSchema, StatusSchema, PresentLocationSchema)
from api.models.parcels import Parcel
from api.helpers.auth import (get_user_identity, admin_required)
from api.helpers.validators import validate_id
from api.helpers.parcel_filters import get_parcel_to_edit


parcel = Parcel()


@api.route('/parcels')
class CreateGetParcelsResource(Resource):

    @jwt_required
    def post(self):
        '''Create parcel'''
        current_user = get_user_identity()
        print(current_user)
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
        response = jsonify(parcels)
        return response


@api.route('/parcels/<parcelId>')
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


@api.route('/users/<userId>/parcels/')
@api.route('/users/<userId>/parcels/<parcelId>')
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
                {"message": f"{current_user['username']} has no {res} ordered."})
            response.status_code = 404
            return response
        return jsonify(parcels)


@api.route('/parcels/<parcelId>/cancel')
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
        return jsonify({"message": f"{current_user['username']} has no parcel of id {parcelId}."})


@api.route('/parcels/<parcelId>/destination')
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
            return jsonify(editted_parcel)
        return jsonify({"message": f"{current_user['username']} has no parcel of id {parcelId}."})


@api.route('/parcels/<parcelId>/status')
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


@api.route('/parcels/<parcelId>/presentLocation')
class EditParcelPresentLocationResource(Resource):

    @jwt_required
    @admin_required
    def put(self, parcelId):
        filter_data = {'id': str(parcelId)}
        parcel_to_edit = get_parcel_to_edit(parcelId, filter_data)
        if parcel_to_edit:
            request_data = request.get_json()
            new_parcel_data = PresentLocationSchema().load_json_data(request_data)
            editted_parcel = parcel.update_parcel(parcelId, **new_parcel_data)
            return jsonify(editted_parcel)
        return jsonify({"message": f"No parcel id {parcelId}."})
