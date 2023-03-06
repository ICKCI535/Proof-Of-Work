from flask_restx import Model, fields
from .utils import generate_from_base_response
from .base import operation_response_model

import sys
sys.path.append("..")
sys.path.append("..")
from core.db.constants import AuthorizeType

connect_account_model = Model('ConnectAccount', {
    "type": fields.Integer(required=True, description="Account type"),
    "externalId": fields.String(attribute='external_id', required=True, description='Account external id'),
    "externalUsername": fields.String(attribute='external_username', required=True, description='Account external username'),
    "externalAvatar": fields.String(attribute='external_avatar', required=True, description='Account avatar')
})

user_model = Model('User', {
    'id': fields.Integer(required=True, description='The user identifier'),
    'username': fields.String(data_key="username", required=True, description='The cat name'),
    'avatar': fields.String(required=True, description='User avatar'),
})

user_model_with_connected_account = user_model.inherit('User',  {
    "connectedAccounts": fields.List(fields.Nested(connect_account_model), attribute="connected_account")
})

update_user_model = Model('UpdateUser', {
    'avatar': fields.String(required=True, description='User avatar'),
})

get_user_response = generate_from_base_response("GetUserResponse", {
    'data': fields.Nested(user_model_with_connected_account),
})

update_user_request = Model.inherit("UpdateUserRequest", update_user_model)

update_user_response = generate_from_base_response("UpdateUserResponse", {
    'data': fields.Nested(user_model),
})

authorize_user_request_model = Model('AuthorizeUserRequest', {
    'authType': fields.String(required=True, enum=[type.value for type in AuthorizeType], description='Authorize type'),
    'identifier': fields.String(required=True, description='Identifier'),
    'signature': fields.String(required=True, description='Authorize signature'),
    'message': fields.String(required=True, description='Authorize message'),
    'timestamp': fields.Integer(required=True, description='Authorize timestamp'),
})

authorized_model = Model('LoggedIn', {
    'accessToken': fields.String(attribute="access_token", required=True, description='Access token'),
    'expiredIn': fields.Integer(attribute="expired_in", required=True, description='Expired in timestamp'),
    'user': fields.Nested(user_model_with_connected_account),
})

authorize_user_response_model = generate_from_base_response("AuthorizeUserResponse", {
    'data': fields.Nested(authorized_model),
})

unbind_account_request = Model("UnbindAccountRequest", {
    "type": fields.Integer(required=True, description="Account type")
})

bind_account_request = Model("BindAccountRequest", {
    "type": fields.String(required=True, enum=[type.value for type in AuthorizeType], description='Authorize type'),
    "code": fields.String(required=False, description="Account authorization code"),
    "externalId": fields.Raw(attribute='external_id'),
    "extra": fields.Raw(),
})

account_bound = Model.inherit("AccountBound", connect_account_model, {
    'extra': fields.Raw()
})

status_quest_response = Model("StatusQuestResponse",{
    "status": fields.Integer(required= True,description = "Quest's status")
})

user_models = [
    connect_account_model,
    user_model,
    status_quest_response,
    user_model_with_connected_account,
    get_user_response,
    update_user_request,
    update_user_response,
    account_bound,
    bind_account_request,
    unbind_account_request,
    authorize_user_request_model,
    authorized_model,
    authorize_user_response_model
]
