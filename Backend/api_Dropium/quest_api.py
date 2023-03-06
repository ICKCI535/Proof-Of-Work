from .models import quest_models,\
    get_quest_response,\
    get_quests_response,\
    verify_quest_request,\
    verify_quest_response
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from flask_restx._http import HTTPStatus
from core.services.quest_service import QuestService
from core.services.task_service import TaskService
from .models.utils import init_models, build_parser
from flask_restx import Namespace, Resource
from core.services.exceptions import ResourceNotFoundException, ResourceExistedException
from .models import operation_response_model
from core.services.task_service import TaskService
from core.services.quest_service import QuestService
from core.db.constants import QuestEntryStatus
import sys
sys.path.append("..")
sys.path.append("..")

api = Namespace('Quests', description='Quests related operation')
init_models(api, quest_models)


@api.route('/')
class Quest(Resource):

    @api.doc('quest')
    @api.response(200, model=get_quests_response, description="Success")
    @api.marshal_with(get_quests_response)
    def get(self):
        '''List quests'''
        quest_service = QuestService()

        quests = quest_service.get_all_quests()
        return {
            "success": True,
            "data": quests
        }


@api.route('/<int:id>')
class Quest(Resource):
    @api.doc('quest')
    @api.response(200, model=get_quest_response, description="Success")
    @api.marshal_with(get_quest_response)
    def get(self, id):
        '''Get a quest by id'''
        quest_service = QuestService()

        quest = quest_service.get_quest_by_id(id)

        if (quest):
            return {
                "success": True,
                "data": quest
            }
        else:
            api.abort(HTTPStatus.NOT_FOUND, {
                "success": False,
            })


@api.route('/<int:quest_id>/tasks/<int:task_id>/verify')
class QuestTaskVerify(Resource):
    @jwt_required(fresh=True)
    @api.doc('quest')
    @api.response(HTTPStatus.OK, model=operation_response_model, description="Success")
    def post(self, quest_id: int, task_id: int):
        '''Verify  task'''

        user_id = get_jwt_identity()

        task_service = TaskService()

        # get quest task and check if it exists
        quest_task = task_service.get_quest_task(task_id=task_id, quest_id=quest_id)

        if (not quest_task):
            raise ResourceNotFoundException("Task not found")

        # get task entry and check if it exists
        task_entry = task_service.get_user_task_entry_status(
            task_id=task_id, quest_id=quest_id, user_id=user_id)

        print(task_entry)
        
        if task_entry and task_entry["status"]:
            return ResourceExistedException("Task already verified")

        #verify task
        is_verified = task_service.verify_task(quest_task, user_id)
        

        #get user task entry and update status
        task_entries = task_service.get_quest_task_entries(quest_id=quest_id, user_id=user_id)

        quest_service = QuestService()

        status = QuestEntryStatus.CLAIMABLE if all(
            [entry["status"] for entry in task_entries]) else QuestEntryStatus.PENDING

        # if all task entries are verified, update the corresponding quest entry status to QuestStatus.CLAIMABLE
        quest_service.upsert_quest_entry(
            quest_id=quest_id, user_id=user_id, status=status)

        # upsert user task entry
        task_service.upsert_task_entry(
            task_id=task_id, quest_id=quest_id, user_id=user_id, status=is_verified)


        return {
            "success": is_verified
        }, HTTPStatus.OK


# @api.route('/test')
# class UserQuest(Resource):
#     # @jwt_required(fresh=True)
#     @ api.doc('users')
#     @ api.response(200, description="Get quest's status  by user")
#     def get(self):
#         '''TEST'''

#         a = os.system('node apis/hello.js')
#         return a
