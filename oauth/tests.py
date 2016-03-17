from django.test import Client, TestCase
import json

# Create your tests here.

class TestOauth(TestCase):
    fixtures = ['users.yaml']

    def test_oauth_callback_url(self):
        c = Client()
        url = '/oauth/facebook/auth'
        data = {
            # 'email': 'a@b.com',
            'access_token': 'abcdef',
            'expiry_date': '2016-03-30',
            'oauth_provider': 'facebook',
            'third_party_user_id': '123123',
        }
        res = c.post(url, json.dumps(data),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            content_type='application/json'
        )
        assert res.status_code == 200



