
import pytest


@pytest.fixture(scope="session")
def test_get_access_token():
    from controller.user import userLogin
    user_details = userLogin({"email":"aanandi@gmail.com","password":"vaishnavi1"})
    yield user_details["data"]["accessToken"]