from flask_restx import Model, fields
from .utils import generate_from_base_response
from .base import operation_response_model

import sys
sys.path.append("..")
sys.path.append("..")
from core.db.constants import RewardType, Eligibility, QuestStatus, SolanaCluster, TaskType

quest_task_model = Model("QuestTask", {
    'id': fields.Integer(required=True, description='The task identifier'),
    'type': fields.String(attribute='type', enum = [type.value for type in TaskType], required=True, description='Task type'),
    'extra': fields.Raw(attribute='extra', required=True, description='Task extra'),
})

create_quest_task_model =  Model("CreateQuestTask", {
    'id': fields.Integer(require = True, description = "Task's identifier"),
    'type': fields.String(attribute='type', enum = [type.value for type in TaskType], required=True, description='Task type'),
    'extra': fields.Raw(attribute='extra', required=True, description='Task extra'),
})

community_object = Model("CommunityObject",{
    'urlSlug': fields.String(attribute = 'url_slug',required=True, description="The community's url slug"),
    "name":fields.String(required = True,description = "The community name"),
    "logo": fields.String(required= True,description = "The community logo")
})

reward_object_request = Model("QuestRewardObject",{
    'type': fields.Integer(required = True,description = "Reward type"),
    'data': fields.Raw(required = True,description="Reward information"),
    'questId': fields.Integer(attribute = "quest_id",equired= True, description = "Quest id")
})

reward_object_response = Model("QuestRewardObject",{
    'id': fields.Integer(required = True, description = "Reward's identifier"),
    'type': fields.Integer(required = True,description = "Reward type"),
    'data': fields.Raw(required = True,description="Reward information"),
    'questId': fields.Integer(attribute = "quest_id",equired= True, description = "Quest id")
})

quest_model = Model('Quest', {
    'id': fields.Integer(required=True, description='The quest identifier'),
    'title': fields.String(required=True, description='The quest title'),
    'description': fields.String(required=True, description='The quest description'),
    'startAt': fields.DateTime(attribute="start_at", dt_format='iso8601', required=True, description='The time quest will be started'),
    'endAt': fields.DateTime(attribute='end_at', dt_format='iso8601', required=True, description='the time quest will be ended'),
    'rewardType': fields.String(attribute='reward_type', enum = [type.value for type in RewardType], required=True, description='Reward type'),
    'rewardSlots': fields.Integer(attribute='reward_slots', required=True, description='Reward slot'),
    'network': fields.String(required=True, enum = [type.value for type in SolanaCluster], description='Network'),
    'eligibility': fields.String(required=True, enum = [type.value for type in Eligibility], description='Eligibility'),
    'status': fields.String(required=True, enum = [type.value for type in QuestStatus], description="Quest's status"),
    "community":fields.Nested(community_object),
    'logo': fields.String(required = True,description = "Quest's logo")
})


create_quest_model = Model('CreateQuest',{
    'title': fields.String(required=True, description='The quest title'),
    'description': fields.String(required=True, description='The quest description'),
    'startAt': fields.DateTime(attribute="start_at", dt_format='iso8601', required=True, description='The time quest will be started'),
    'endAt': fields.DateTime(attribute='end_at', dt_format='iso8601', required=True, description='the time quest will be ended'),
    'rewardType': fields.String(attribute='reward_type', enum = [type.value for type in RewardType], required=True, description='Reward type'),
    'rewardSlots': fields.Integer(attribute='reward_slots', required=True, description='Reward slot'),
    'network': fields.String(required=True, enum = [type.value for type in SolanaCluster], description='Network'),
    'eligibility': fields.String(required=True, enum = [type.value for type in Eligibility], description='Eligibility'),
    'logo': fields.String(required = True,description = "Quest's logo"),
    'tasks': fields.List(fields.Nested(create_quest_task_model), require=True, description='tasks in quest'),
    'rewardList':fields.List(fields.Nested(reward_object_request),attribute = "reward_list",required = True, description = "Reward list of quest")
})

update_quest_model = Model('UpdateQuest',{
    'title': fields.String(required=True, description='The quest title'),
    'description': fields.String(required=True, description='The quest description'),
    'startAt': fields.DateTime(attribute="start_at", dt_format='iso8601', required=True, description='The time quest will be started'),
    'endAt': fields.DateTime(attribute='end_at', dt_format='iso8601', required=True, description='the time quest will be ended'),
    'rewardType': fields.String(attribute='reward_type', enum = [type.value for type in RewardType], required=True, description='Reward type'),
    'rewardSlots': fields.Integer(attribute='reward_slots', required=True, description='Reward slot'),
    'network': fields.String(required=True, enum = [type.value for type in SolanaCluster], description='Network'),
    'eligibility': fields.String(required=True, enum = [type.value for type in Eligibility], description='Eligibility'),
    'logo': fields.String(required = True,description = "Quest's logo"),
    'tasks': fields.List(fields.Nested(create_quest_task_model), require=True, description='tasks in quest'),
    'rewardList':fields.List(fields.Nested(reward_object_response),attribute = "reward_list",required = True, description = "Reward list of quest")
})

quest_model_with_tasks = Model("QuestWithTasks", {
    'id': fields.Integer(required=True, description='The quest identifier'),
    'title': fields.String(required=True, description='The quest title'),
    'description': fields.String(required=True, description='The quest description'),
    'startAt': fields.DateTime(attribute="start_at", dt_format='iso8601', required=True, description='The time quest will be started'),
    'endAt': fields.DateTime(attribute='end_at', dt_format='iso8601', required=True, description='the time quest will be ended'),
    'rewardType': fields.String(attribute='reward_type', enum = [type.value for type in RewardType], required=True, description='Reward type'),
    'rewardSlots': fields.Integer(attribute='reward_slots', required=True, description='Reward slot'),
    'network': fields.String(required=True, enum = [type.value for type in SolanaCluster], description='Network'),
    'eligibility': fields.String(required=True, enum = [type.value for type in Eligibility], description='Eligibility'),
    'status': fields.String(required=True, enum = [type.value for type in QuestStatus], description="Quest's status"),
    "community":fields.Nested(community_object),
    'logo': fields.String(required = True,description = "Quest's logo"),
    'tasks': fields.List(fields.Nested(quest_task_model), require=True, description='tasks in quest'),
    'rewardList':fields.List(fields.Nested(reward_object_response),attribute = "reward_list",required = True, description = "Reward list of quest")
})



get_quest_response = generate_from_base_response("GetQuestResponse", {
    'data': fields.Nested(quest_model_with_tasks),
})

get_quests_response = generate_from_base_response("GetQuestsResponse", {
    'data': fields.List(fields.Nested(quest_model)),
})

create_quest_request = Model("CreateQuestRequest", create_quest_model)

create_quest_response = generate_from_base_response("CreateQuestResponse", {
    'data': fields.Nested(create_quest_model),
})

update_quest_request = Model("UpdateQuestRequest", update_quest_model )

update_quest_response = generate_from_base_response("UpdateQuestResponse", {
    'data': fields.Nested(quest_model_with_tasks),
})

verify_quest_request = Model("VerifyQuestRequest", {
    'id': fields.Integer(required=True, description='The quest identifier'),
    'userId': fields.String(required=True, description="The user identifier"),
})

verify_quest_response = Model("VerifyQuestResponse",operation_response_model)

quests_by_user_response = generate_from_base_response("QuestsByUser",{
    "data" : fields.List(fields.Nested(quest_model))
})

quest_models = [
    quest_task_model,
    quest_model,
    quest_model_with_tasks,
    create_quest_model,
    reward_object_request,
    update_quest_model,
    community_object,
    create_quest_task_model,
    get_quest_response,
    get_quests_response,
    create_quest_request,
    create_quest_response,
    update_quest_request,
    update_quest_response,
    verify_quest_request,
    verify_quest_response,
    quests_by_user_response
]
