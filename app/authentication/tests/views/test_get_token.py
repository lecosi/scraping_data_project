import faker
from fastapi.testclient import TestClient
from fastapi import status

from main import app

fake = faker.Faker()


class TestGetToken:
    ENDPOINT = '/login/'

    def test_get_token_success(
        self,
        user_initial
    ):
        user = user_initial
        client = TestClient(app)
        response = client.post(
            self.ENDPOINT,
            data=dict(
                username=user.username,
                password='123456'
            )
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert response_data['access_token']
        assert response_data['refresh_token']
        assert response_data['expires']

    def test_when_username_is_invalid(self):
        client = TestClient(app)
        response = client.post(
            self.ENDPOINT,
            data=dict(
                username=f'{fake.first_name()}_{fake.last_name()}',
                password=fake.password()
            )
        )
        expected_data = {
            'component': 'Authentication',
            'msg': 'username or password is incorrect'
        }
        response_data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data == expected_data

    def test_when_password_is_invalid(
        self,
        user_initial
    ):
        user = user_initial
        client = TestClient(app)
        response = client.post(
            self.ENDPOINT,
            data=dict(
                username=user.username,
                password=fake.password()
            )
        )
        expected_data = {
            'component': 'Authentication',
            'msg': 'username or password is incorrect'
        }
        response_data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data == expected_data

    def test_when_user_is_inactive(
        self,
        user_initial
    ):
        user = user_initial
        user.is_active = False
        user.save()

        client = TestClient(app)
        response = client.post(
            self.ENDPOINT,
            data=dict(
                username=user.username,
                password=fake.password()
            )
        )
        expected_data = {
            'component': 'Authentication',
            'msg': 'user is inactive'
        }
        response_data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data == expected_data

    def test_username_in_request_not_exists(
        self,
        user_initial
    ):
        client = TestClient(app)
        response = client.post(
            self.ENDPOINT,
            data=dict(
                password='123456'
            )
        )
        expected_data = {'username': ['This field is required.']}
        response_data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data == expected_data

    def test_password_in_request_not_exists(
        self,
        user_initial
    ):
        user = user_initial
        client = TestClient(app)
        response = client.post(
            self.ENDPOINT,
            data=dict(
                username=user.username
            )
        )
        expected_data = {'password': ['This field is required.']}
        response_data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data == expected_data
