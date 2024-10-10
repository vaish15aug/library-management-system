import pytest
from controller.user import createUser, userLogin, updateUser, delete_user, get_user, user_logout
from fastapi import HTTPException
from fastapi.testclient import TestClient
from main import app  

client = TestClient(app)


# 1) create user
@pytest.mark.parametrize("data", [
    ({"name":"Aish", "email": "a@gmail.com", "password": "vaishnavi1", "phone": "7896541200"}),
])
def test_createUser(data):
    user_details = createUser(data)
    assert user_details['status'] == 201, f"user not created => {data}"

# missing email
@pytest.mark.parametrize("data", [
    ({"name":"Aish", "password": "vaishnavi1", "phone": "7896541200"}),
])
def test_create_user_missing_email(data):
    with pytest.raises(HTTPException) as exc_info:
        createUser(data)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Email is required"

# missing password
@pytest.mark.parametrize("data", [
    ({"name":"A", "email": "aa@gmail.com", "phone": "7896541200"}),
])
def test_create_user_missing_password(data):
    with pytest.raises(HTTPException) as exc_info:
        createUser(data)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Password is required"

# missing name
@pytest.mark.parametrize("data", [
    ({"email": "aa@gmail.com", "password": "vaishnavi1", "phone": "7896541200"}),
])
def test_create_user_missing_name(data):
    with pytest.raises(HTTPException) as exc_info:
        createUser(data)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Name is required"

# missing phone
@pytest.mark.parametrize("data", [
    ({"name":"A", "email": "aa@gmail.com", "password": "vaishnavi1"}),
])
def test_create_user_missing_phone(data):
    with pytest.raises(HTTPException) as exc_info:
        createUser(data)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Phone number is required"

# ///////////////////////////////////////////////////////////////////////////////////////////////////
  
# 2) login user


def test_user_data(test_get_access_token):
    print("test_get_access_token ->>",test_get_access_token)

def test_user_data1(test_get_access_token):
    print("test_user_data1 ->>", test_get_access_token)
   

# Successful login
@pytest.mark.parametrize("data", [
    ({"email": "aanandi@gmail.com", "password": "vaishnavi1"}),
])
def test_user_login_success(data):
    response = userLogin(data)  
    assert response['status'] == 200, f"Login failed => {data}"
    assert response['message'] == "Login successful"
    assert "accessToken" in response["data"]
    assert "refreshToken" in response["data"]

# Missing email
@pytest.mark.parametrize("data", [
    ({"password": "vaishnavi1"}),
])
def test_user_login_missing_email(data):
    with pytest.raises(HTTPException) as exc_info:
        userLogin(data)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Email is required"

# Missing password
@pytest.mark.parametrize("data", [
    ({"email": "aanandi@gmail.com"}),
])
def test_user_login_missing_password(data):
    with pytest.raises(HTTPException) as exc_info:
        userLogin(data)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Password is required"

# Non-existing user
@pytest.mark.parametrize("data", [
    ({"email": "nonexisting@gmail.com", "password": "wrongpassword"}),
])
def test_user_login_user_not_found(data):
    with pytest.raises(HTTPException) as exc_info:
        userLogin(data)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"


# user update 
# name, phone 
@pytest.mark.parametrize("data","payload"[({
   "id":"39", "name":"aish","phone":"7456321077"})
    ])
def test_user_update(data):
    with pytest.raises(HTTPException) as exc_info:
        updateUser(data)
    assert exc_info.value.status_code == 200
    assert exc_info.value.detail == "user updated successfully"






