from flask_restx import Api

from .user_api import api as user_api
from .community_api import api as community_api
from .quest_api import api as quest_api

authorizations = {
    'bearerAuth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
    }
}

api = Api(
    title='Dropium',
    version='1.0',
    description='Dropium API',
    authorizations=authorizations,
    security="bearerAuth",
    # All API metadatas
    prefix="/api"
)
api.add_namespace(user_api, path="/users")
api.add_namespace(quest_api, path="/quests")
api.add_namespace(community_api,path="/communities")
