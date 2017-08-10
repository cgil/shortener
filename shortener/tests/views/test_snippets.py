import datetime

from shortener.lib import url_lib
from shortener.models.snippet import Snippet
from shortener.tests import factories
from shortener.tests.base import ViewTestCase


class SnippetTestCase(ViewTestCase):

    def setUp(self):
        super(SnippetTestCase, self).setUp()
        self.model_factory = factories.SnippetFactory
        self.model = Snippet
        self.url_prefix = 'snippets'

    def test_get(self):
        """Test that we can get a record."""
        record = self.model_factory()
        res = self.get(
            '/{}/{}'.format(
                self.url_prefix,
                record.id,
            ),
        )
        assert res.data['data']['id'] == str(record.id)
        assert res.status_code == 200

    def test_get_404(self):
        """Test that we can handle record 404's."""
        res = self.get(
            '/{}/{}'.format(
                self.url_prefix,
                12345,
            ),
        )
        assert res.status_code == 404

    def test_get_soft_deleted(self):
        """Test that we can get a record."""
        record = self.model_factory()
        record.deleted_at = datetime.datetime.utcnow()
        res = self.get(
            '/{}/{}'.format(
                self.url_prefix,
                record.id
            ),
        )
        assert res.status_code == 404

    def test_get_list(self):
        """Test that we can get a record."""
        records = self.model_factory.create_batch(size=3)
        res = self.get(
            '/{}/'.format(self.url_prefix),
        )
        assert res.status_code == 200
        found = self.model.query.all()
        assert len(found) == 3
        found = sorted(found, key=lambda p: p.id)
        records = sorted(records, key=lambda p: p.id)
        for i, f in enumerate(found):
            assert found[i].id == records[i].id

    def test_get_list_soft_deleted(self):
        """Test that we can get a record."""
        records = self.model_factory.create_batch(size=3)
        for record in records:
            record.deleted_at = datetime.datetime.utcnow()
        res = self.get(
            '/{}/'.format(self.url_prefix),
        )
        assert res.status_code == 200
        assert not res.data['data']

    def test_post(self):
        """Test that we can create a new record."""
        attrs = self.model_factory.build()
        del attrs['id']
        data = {
            'data': {
                'attributes': attrs,
                'type': '{}'.format(self.url_prefix),
            }
        }
        res = self.post(
            '/{}/'.format(self.url_prefix),
            data=data,
        )
        for k, v in attrs.iteritems():
            if k == 'short_url':
                assert (
                    res.data['data']['attributes'][k] ==
                    url_lib.encode_short_url(int(res.data['data']['id']))
                )
            else:
                assert res.data['data']['attributes'][k] == v
        assert res.status_code == 201

    def test_delete(self):
        """Test that we can delete a record."""
        record = self.model_factory()
        assert len(self.model.query.all()) == 1
        res = self.delete(
            '/{}/{}'.format(self.url_prefix, record.id),
        )
        found = self.model.query.all()
        assert len(found) == 1
        assert found[0].deleted_at is not None
        assert res.status_code == 204
        assert not res.data

    def test_patch(self):
        """Test that we can patch a record."""
        record = self.model_factory()
        build_attrs = self.model_factory.build()
        del build_attrs['id']

        data = {
            'data': {
                'attributes': build_attrs,
                'type': '{}'.format(self.url_prefix),
                'id': str(record.id),
            }
        }
        res = self.patch(
            '/{}/{}'.format(self.url_prefix, record.id),
            data=data,
        )
        assert res.status_code == 200
        for k, v in build_attrs.iteritems():
            assert res.data['data']['attributes'][k] == v
