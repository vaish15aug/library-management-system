
import pytest


@pytest.fixture(scope="session")
def test_get_access_token():
    from controller.user import userLogin
    user_details = userLogin({"email":"aanandi@gmail.com","password":"vaishnavi1"})
    yield user_details["data"]["accessToken"]

@pytest.fixture(scope="session")
def test_get_admin_access_token():
    from controller.admin import adminLogin
    admin_details = adminLogin({"name":"vaishnavi", "email":"vaishnavi@gmail.com", "password":"vaish1", "phone":"985641230","is_super":True})
    yield admin_details["data"]["accessToken"]

