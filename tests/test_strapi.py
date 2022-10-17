import unittest
import urllib.parse

from strapisdk.strapi import Strapi
from strapisdk.config import (STRAPI_IDENTIFIER, STRAPI_PASSWORD, STRAPI_TEST_COLLECTION, STRAPI_TEST_COLLECTION_ID)


class StrapiTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.strapi = Strapi()
        self.is_logged = False
        self.login_data = None
        self.test_collection = STRAPI_TEST_COLLECTION
        self.test_collection_id = STRAPI_TEST_COLLECTION_ID

    def execute_login(self):
        if not self.is_logged:
            data = self.strapi.login(identifier=STRAPI_IDENTIFIER, password=STRAPI_PASSWORD)
            self.login_data = data
        self.is_logged = True
        return self.login_data

    def test_login(self):
        data = self.execute_login()
        self.assertIn('jwt', data)
        self.assertIsInstance(self.strapi.jwt, str)

    def test_remove_token(self):
        self.execute_login()
        self.assertIsInstance(self.strapi.jwt, str)
        self.assertIn('Authorization', self.strapi.session.headers)
        self.strapi.jwt = ""
        self.assertEqual(self.strapi.jwt, "")
        self.assertNotIn('Authorization', self.strapi.session.headers)

    def test_fetch_user(self):
        self.execute_login()
        self.assertIn('id', self.strapi.fetch_user())

    def test_find(self):
        self.execute_login()
        output = self.strapi.find(self.test_collection, params={
            'filters': {
                'ack': {
                    '$eq': 'sent'
                }
            }
        })
        self.assertIn('data', output)
        self.assertIn('meta', output)
        data = output.get("data", {})
        self.assertIsInstance(data, list)

    def test_find_one(self):
        self.execute_login()
        output = self.strapi.find_one(self.test_collection, self.test_collection_id, {'fields': ['id']})
        self.assertIn('data', output)
        self.assertIn('meta', output)
        data = output.get("data", {})
        self.assertIn('id', data)
        self.assertIn('attributes', data)
        attributes = data.get("attributes", {})
        total_keys = len(attributes.keys())
        self.assertEqual(total_keys, 0)
        output = self.strapi.find_one(self.test_collection, self.test_collection_id)
        data = output.get("data", {})
        attributes = data.get("attributes", {})
        total_keys = len(attributes.keys())
        self.assertGreater(total_keys, 1)


if __name__ == '__main__':
    unittest.main()
