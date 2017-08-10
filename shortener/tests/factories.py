import logging

import factory
from sqlalchemy.exc import InvalidRequestError

from shortener.lib.database import db
from shortener.models.snippet import Snippet

logging.getLogger('factory').setLevel(logging.ERROR)


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):

    """Base Factory."""

    class Meta:
        abstract = True
        sqlalchemy_session = db.session

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        """Returns a dictionary of a built object."""
        for k in kwargs.keys():
            if k in model_class.relationships():
                rel_key = '{}_id'.format(k)
                try:
                    kwargs[rel_key] = str(kwargs[k].id)
                except AttributeError:
                    pass
        obj = super(BaseFactory, cls)._build(model_class, *args, **kwargs)
        obj_dict = obj.to_dict()
        try:
            db.session.expunge(obj)
        except InvalidRequestError:
            pass
        return obj_dict

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Overrides create strategy, commits on create"""
        for k in kwargs.keys():
            if k in model_class.relationships():
                rel_key = '{}_id'.format(k)
                kwargs[rel_key] = str(kwargs[k].id)
        obj = super(BaseFactory, cls)._create(model_class, *args, **kwargs)
        obj.save(obj)
        return obj


class SnippetFactory(BaseFactory):

    class Meta:
        model = Snippet

    desktop_redirect = factory.Sequence(lambda n: 'https://www.desktop.com/test_{0}'.format(n))
    desktop_redirect_count = factory.Sequence(lambda n: n)
    mobile_redirect = factory.Sequence(lambda n: 'https://www.mobile.com/test_{0}'.format(n))
    mobile_redirect_count = factory.Sequence(lambda n: n)
    tablet_redirect = factory.Sequence(lambda n: 'https://www.tablet.com/test_{0}'.format(n))
    tablet_redirect_count = factory.Sequence(lambda n: n)
    short_url = factory.Sequence(lambda n: 'https://www.short.com/test_{0}'.format(n))
