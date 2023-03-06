from flask_restx import Model, fields
from .utils import generate_from_base_response
from .base import operation_response_model

community_model = Model('Community', {
    # 'communityId': fields.Integer(attribute='community_id', required=True, description='The community identifier'),
    # 'communityUrl': fields.String(attribute='community_url', required=True, description='The community url'),
    # 'communityName': fields.String(attribute='community_name', required=True, description='The community name'),
    # 'communityLogo': fields.String(attribute='community_logo', required=True, description='The community logo'),
    # 'communityBackground': fields.String(attribute='community_background', required=True, description='The community background'),
    # 'communityIntroduction': fields.String(rattribute='community_introduction', equired=True, description='The community introduction'),
    # 'communityExtra': fields.String(attribute='community_extra', required=True, description='The community extra'),
    # 'communityTwitterUid': fields.String(attribute='community_twitter_uid', required=True, description='The community twitter uid'),
    # 'communityTwitterName': fields.String(attribute='community_twitter_name', required=True, description="The community twitter's name"),
    # 'communityTwitterUsername': fields.String(attribute='community_twitter_username', required=True, description="The community twitter's username"),
    # 'creatorUserId': fields.Integer(attribute='creator_user_id', required=True, description="The community's creator identifier"),
    # 'followersCount': fields.Integer(attribute='followers_count', required=True, description='The number of followers'),
    # 'email': fields.Integer(required=True, description='Email'),
    'urlSlug': fields.String(attribute = 'url_slug',required = True, description = "The community's url slug"),
    'name': fields.String(required = True, description = "The community's name"),
    'logo': fields.String(required = True, description = "The community's logo"),
    'description': fields.String(required = True, description = "The community's description"),
    'cover': fields.String(required = True, description = "The community's cover"),
    'owner_id' : fields.Integer(attribute = 'owner_id',required = True, description = 'The community identifier'),
    
    
})

get_community_response = generate_from_base_response("GetCommunityResponse", {
    'data': fields.Nested(community_model),
})

create_community_request = Model("CreateCommunityRequest", {
    'urlSlug': fields.String(attribute = 'url_slug',required = True, description = "The community's url slug"),
    'name': fields.String(required = True, description = "The community's name"),
    'logo': fields.String(required = True, description = "The community's logo"),
    'description': fields.String(required = True, description = "The community's description"),
    'cover': fields.String(required = True, description = "The community's cover"),
    })

create_community_response = generate_from_base_response("CreateCommunityResponse", {
    'data': fields.Nested(community_model),
})

update_community_request = Model(
    "UpdateCommunityRequest", {
        'urlSlug': fields.String(attribute = 'url_slug',required = True, description = "The community's url slug"),
        'name': fields.String(required = True, description = "The community's name"),
        'logo': fields.String(required = True, description = "The community's logo"),
        'description': fields.String(required = True, description = "The community's description"),
        'cover': fields.String(required = True, description = "The community's cover"),
    })

update_community_response = generate_from_base_response("UpdateCommunityResponse", {
    'data': fields.Nested(community_model),
})

community_models = [
    community_model,
    get_community_response,
    create_community_request,
    create_community_response,
    update_community_request,
    update_community_response
]
