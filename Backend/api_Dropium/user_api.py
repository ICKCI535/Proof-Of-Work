from core.db.constants import AuthorizeType
from core.services.user_service import UserService
from core import AuthorizationException
from core.services.quest_service import QuestService
from core.services.community_service import CommunityService
from core.services.exceptions import ResourceExistedException, ResourceNotFoundException
from .models.utils import init_models, build_parser
from flask_restx import Namespace, Resource, marshal
from flask_restx._http import HTTPStatus
from flask_jwt_extended import create_access_token, decode_token, jwt_required, get_jwt_identity
from .models import user_models,\
    authorize_user_request_model,\
    authorize_user_response_model,\
    get_community_response,\
    bind_account_request,\
    status_quest_response,\
    unbind_account_request,\
    get_user_response,\
    update_user_request,\
    update_user_response,\
    operation_response_model,\
    quests_by_user_response,\
    error_response_model,\
    error

from .exceptions import IdentityNotMatchException
import datetime

import sys
sys.path.append("..")
sys.path.append("..")

api = Namespace('Users', description='Users related operation')
models = user_models
models.append(operation_response_model)
models.append(error_response_model)
models.append(error)
init_models(api, models)


@api.route('/<int:id>')
class User(Resource):
    @jwt_required(fresh=True)
    @api.doc('users')
    @api.response(HTTPStatus.OK, model=get_user_response, description="Get success")
    @api.marshal_with(get_user_response)
    def get(self, id):
        '''Get user by id'''

        identity = get_jwt_identity()
        if (not id == int(identity)):
            raise IdentityNotMatchException()

        user_service = UserService()

        user = user_service.get_user_by_id(id, external_included=True)

        if (not user):
            api.abort(404, {
                "success": False,
                "data": {
                    "message": " User not found."
                }
            })

        return {
            "success": True,
            "data": user
        }

    @jwt_required(fresh=True)
    @api.doc('users')
    @api.expect(update_user_request)
    @api.response(HTTPStatus.OK, model=update_user_response, description="Update success")
    @api.marshal_with(update_user_response)
    def put(self, id):
        '''Update user'''
        identity = get_jwt_identity()
        if (not id == int(identity)):
            raise IdentityNotMatchException()

        parser = build_parser(update_user_request)
        request = parser.parse_args()

        user_service = UserService()

        updated_user = user_service.update_user(id, request)

        return {
            "success": True,
            "data": updated_user
        }


@api.route('/<int:id>/bind')
class UserBind(Resource):
    @jwt_required(fresh=True)
    @api.doc('users')
    @api.expect(bind_account_request)
    @api.response(HTTPStatus.CREATED, model=operation_response_model, description="Bind success")
    @api.response(HTTPStatus.NOT_FOUND, model=error_response_model, description="Not foiund")
    @api.response(HTTPStatus.BAD_REQUEST, model=error_response_model, description="Bad request")
    def post(self, id):
        '''Bind an external account to user'''
        identity = get_jwt_identity()
        if (not id == int(identity)):
            raise IdentityNotMatchException()


        parser = build_parser(bind_account_request)
        args = parser.parse_args()
        authType: AuthorizeType = AuthorizeType.from_str(args["type"])

        if not authType.connect_account_authorize_allowed():
            raise AuthorizationException("Authorization type not allowed")

        user_service = UserService()

        user_service.bind_external_account(
            type=authType, code=args["code"], external_id=args["externalId"], user_id=identity, extra=args["extra"])

        return {"success": True}, HTTPStatus.CREATED


@api.route('/<int:id>/unbind')
class UserUnbind(Resource):
    @jwt_required(fresh=True)
    @api.doc('users')
    @api.expect(unbind_account_request)
    @api.response(HTTPStatus.OK, model=operation_response_model, description="Unbind success")
    @api.response(HTTPStatus.NOT_FOUND, model=error_response_model, description="Resource not found")
    def post(self, id):
        identity = get_jwt_identity()
        if (not id == int(identity)):

            raise IdentityNotMatchException()

        parser = build_parser(unbind_account_request)
        args = parser.parse_args()

        user_service = UserService()
        user_service.unbind_external_account(type=args["type"], user_id=identity)

        return {"success": True}, HTTPStatus.OK


@api.route('/authorize/prepare')
class UserPrepareAuthorization(Resource):
    @api.doc('users')
    @api.expect(authorize_user_request_model)
    # @api.response(HTTPStatus.OK, model=authorize_user_response_model, description="Authorize success")
    # @api.marshal_with(authorize_user_response_model)
    def post(self):
        ''' Prepare authorize'''

        parser = build_parser(authorize_user_request_model)
        args = parser.parse_args()
        authType: AuthorizeType = AuthorizeType.from_str(args["authType"])

        user_service = UserService()

        message = user_service.prepare_auth(authType, args)

        return {
            "success": True,
            "data": message
        }


@api.route('/authorize')
class UserAuthorization(Resource):
    @api.doc('users')
    @api.doc(security=[])
    @api.expect(authorize_user_request_model)
    @api.response(HTTPStatus.OK, model=authorize_user_response_model, description="Authorize success")
    @api.marshal_with(authorize_user_response_model)
    def post(self):
        '''Authorize user'''
        parser = build_parser(authorize_user_request_model)
        args = parser.parse_args()
        print(args)
        authType: AuthorizeType = AuthorizeType.from_str(args["authType"])
        if (not authType.direct_authorize_allowed()):
            
            raise AuthorizationException("Authorization type not allowed")

        user_service = UserService()
        try:
            user = user_service.authorize_by_external(
                authType, args["identifier"], args)

            access_token = create_access_token(
                identity=user["id"],
                additional_claims={
                    "authType": args["authType"],
                    "externalId": args["identifier"]
                },
                fresh=True,
                expires_delta=datetime.timedelta(hours=1))

            decoded = decode_token(access_token)    

            return {
                "success": True,
                "data": {
                    "access_token": access_token,
                    "expired_in": decoded["exp"],
                    "user":user
                }
            }
        except AuthorizationException as e:
            api.abort(HTTPStatus.UNAUTHORIZED, str(e))





@api.route('/<int:user_id>/quests/<int:quest_id>')
class UserQuest(Resource):
    # @jwt_required(fresh=True)
    @ api.doc('users')
    @ api.response(200, model=status_quest_response, description="Get quest's status  by user")
    @ api.marshal_with(status_quest_response)
    def get(self, quest_id, user_id):
        '''Quest's status by user'''

        # if quest = None

        quest_service = QuestService()
        quest = quest_service.get_status_of_quest_by_user(
            quest_id=quest_id, user_id=user_id)
        if quest == None:
            api.abort(404, "Quest entry not found")
        return quest

@api.route('/<int:id>/communities')
class UserCommunity(Resource):
    @api.doc('user')
    @api.response(200, model=get_community_response, description="Success")
    @api.marshal_with(get_community_response)
    def get(self,id):
        "List all communities created by user"
        community_service = CommunityService()
        all_communities = community_service.get_communinty_by_owner(id=id)
        return {
            "success": True,
            "data": all_communities
        }