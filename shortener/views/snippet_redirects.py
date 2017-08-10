from flask import Blueprint
from flask import abort
from flask import redirect
from flask import request
from flask_restful import Api
from sqlalchemy.exc import SQLAlchemyError

from shortener.lib import device_detection
from shortener.lib import loggers
from shortener.lib import url_lib
from shortener.models.snippet import Snippet
from shortener.views.base import BaseAPI

logger = loggers.get_logger(__name__)

snippet_redirects_blueprint = Blueprint('snippet_redirects', __name__)
api = Api(snippet_redirects_blueprint)


class SnippetRedirectsAPI(BaseAPI):

    model = Snippet

    def get(self, encoded_id):
        """Redirect based on the given snippet."""
        logger.info({
            'msg': 'Getting the redirect url for the given snippet.',
            'view': self.__class__.__name__,
            'method': 'get',
            'encoded_id': encoded_id,
        })
        try:
            decoded_id = url_lib.decode_short_url(encoded_id)
        except ValueError as e:
            logger.error({
                'msg': 'Improper short url given, aborting.',
                'view': self.__class__.__name__,
                'method': 'get',
                'encoded_id': encoded_id,
                'error': str(e),
            })
            # Improper short url given, 404
            abort(404)

        record = self.model.get_or_404(decoded_id)
        device = device_detection.detect(request)

        # Set the redirect url based on the device type.
        if device == device_detection.MOBILE and record.mobile_redirect:
            redirect_url = record.mobile_redirect
            record.mobile_redirect_count += 1
        elif device == device_detection.TABLET and record.tablet_redirect:
            redirect_url = record.tablet_redirect
            record.tablet_redirect_count += 1
        else:
            redirect_url = record.desktop_redirect
            record.desktop_redirect_count += 1

        try:
            record.save(record)
        except SQLAlchemyError as e:
            logger.error({
                'msg': 'Error updating redirect counter.',
                'view': self.__class__.__name__,
                'method': 'get',
                'encoded_id': encoded_id,
                'redirect_url': redirect_url,
                'error': str(e),
            })
            abort(500)

        return redirect(redirect_url)

    def delete(self, encoded_id):
        pass

    def patch(self, encoded_id):
        pass


api.add_resource(SnippetRedirectsAPI, '/<encoded_id>')
