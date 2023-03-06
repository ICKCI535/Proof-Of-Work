from .base import base_response_model
from flask_restx import Namespace, Model, inputs, abort
from flask_restx.reqparse import RequestParser
from flask_restx._http import HTTPStatus

def init_models(self: Namespace, models: list[Model]):
    self.add_model(base_response_model.name, base_response_model)

    for model in models:
        self.add_model(model.name, model)


def generate_from_base_response(name:str, child: Model):
    return  Model.inherit(name, base_response_model, child)

def marshall_to_base_response(name:str, child: Model):
    pass


def build_parser(model: Model) -> RequestParser:
    parser = RequestParser()
    
    for prop, field in model.items():
        conf = field.schema()
        if conf.get('type') == 'string' and conf.get('format') == 'date-time':
            parser.add_argument(prop, type=inputs.datetime_from_iso8601)
        elif conf['type'] == 'integer':
            parser.add_argument(prop, type=int)
        elif conf['type'] == 'boolean':
            parser.add_argument(prop, type=bool, default=False)
        elif conf['type'] == 'array':
            parser.add_argument(prop, type = dict, action='append')
        else:
            parser.add_argument(prop)
    return parser
