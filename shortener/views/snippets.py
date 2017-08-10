from flask import Blueprint
from flask import request
from flask_restful import Api
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from shortener.lib import loggers
from shortener.lib import url_lib
from shortener.lib.database import db
from shortener.models.snippet import Snippet
from shortener.schemas.snippets_schema import SnippetsSchema
from shortener.views.base import BaseAPI
from shortener.views.base import BaseListAPI

logger = loggers.get_logger(__name__)


snippets_blueprint = Blueprint('snippets', __name__, url_prefix='/snippets')
api = Api(snippets_blueprint)


class SnippetsListAPI(BaseListAPI):

    model = Snippet
    schema_model = SnippetsSchema

    def post(self):
        """Create a new record."""
        logger.info({
            'msg': 'Creating a new record.',
            'view': self.__class__.__name__,
            'method': 'post',
            'schema_model': self.schema_model.__name__,
            'model': self.model.__name__,
        })
        raw_dict = request.get_json(force=True)

        try:
            self.schema.validate(raw_dict)
            attrs = raw_dict['data'].get('attributes') or {}

            record = self.model(**attrs)
            db.session.add(record)
            # Flush to get a record id
            db.session.flush()

            short_url = url_lib.encode_short_url(record.id)
            record.short_url = short_url
            record.save(record)
            query = self.model.get(record.id)
            result = self.schema.dump(query).data
            return result, 201

        except ValidationError as e:
                logger.error({
                    'msg': 'Error validating new record.',
                    'view': self.__class__.__name__,
                    'method': 'post',
                    'schema_model': self.schema_model.__name__,
                    'model': self.model.__name__,
                    'raw_dict': raw_dict,
                    'error': str(e)
                })
                return {'error': e.messages}, 403

        except SQLAlchemyError as e:
                logger.error({
                    'msg': 'Error creating new record.',
                    'view': self.__class__.__name__,
                    'method': 'post',
                    'schema_model': self.schema_model.__name__,
                    'model': self.model.__name__,
                    'raw_dict': raw_dict,
                    'error': str(e)
                })
                db.session.rollback()
                return {'error': str(e)}, 403


class SnippetsAPI(BaseAPI):

    model = Snippet
    schema_model = SnippetsSchema

api.add_resource(SnippetsListAPI, '/')
api.add_resource(SnippetsAPI, '/<id>')
