import pytest
from controller.user import createUser, userLogin, updateUser, delete_user, get_user, user_logout
from fastapi import HTTPException
from fastapi.testclient import TestClient
from main import app  
from schema.user import UserUpdate

client = TestClient(app)


# # 1) create user
# @pytest.mark.parametrize("data", [
#     ({"name":"Aish", "email": "a@gmail.com", "password": "vaishnavi1", "phone": "7896541200"}),
# ])
# def test_createUser(data):
#     user_details = createUser(data)
#     assert user_details['status'] == 201, f"user created => {data}"

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
    assert response['message'] == "Login successfull"
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

# ////////////////////////////////////////////////////////////////////////////////////////////////////////


# 3)user update (name, phone)

@pytest.mark.parametrize("id, data", [
    ("27", { "name": "Aishu1", "phone": "7896541200" }),
])
def test_user_update(id, data):
    payload = {"id": id}
    request_data = UserUpdate(**data) 

    response = updateUser(request_data, payload)

    assert response["status"] == 201
    assert response["message"] == "User update Successfully"


# user not found


@pytest.mark.parametrize("id, data", [
    (1, {"name": "Sakshi","phone": "7896541200"}), 
])
def test_admin_update_user_not_found(id, data):
    payload = {"id": id} 
    with pytest.raises(HTTPException) as exc_info:
        updateUser(UserUpdate(**data), payload)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"

# only name , phone can be updated 
@pytest.mark.parametrize("id, data", [
   (7, {}),
])
def test_user_name_phone_can_be_updated(id, data):
    payload = {"id": id} 

    with pytest.raises(HTTPException) as exc_info:
        updateUser(UserUpdate(**data), payload)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Only name, phone number can be updated"

# Test for updating  name
@pytest.mark.parametrize("id, data", [
    (29, { "name": "Aishwarya ulhe" }),
])
def test_user_name_can_be_updated(id, data):
    payload = {"id": id} 

    response = updateUser(UserUpdate(**data), payload)

    assert response["status"] == 201
    assert response["message"] == "User update Successfully"

# test for updating phone 
@pytest.mark.parametrize("id, data", [
    (29, { "phone": "789600000" }),
])
def test_user_phone_can_be_updated(id, data):
    payload = {"id": id} 

    response = updateUser(UserUpdate(**data), payload)

    assert response["status"] == 201
    assert response["message"] == "User update Successfully"


# ///////////////////////////////////////////////////////////////////////////////////////////////////


# 4) find user

# user found successfully
@pytest.mark.parametrize("id", [
    27,  
])
def test_user_found_successfully(id):
    response = get_user(id)

    assert response["status"] == 200
    assert response["message"] == "User found successfully"


# id must be provided
@pytest.mark.parametrize("id", [
    (),
])
def test_user_id_must_be_provided(id):
    with pytest.raises(HTTPException) as exc_info:        
        get_user(id)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Please provide valid id"


# user not found
@pytest.mark.parametrize("id", [
    45,  
])  
def test_user_not_found(id):    
    with pytest.raises(HTTPException) as exc_info:
        get_user(id)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"




# /////////////////////////////////////////////////////////////////////////////////////////////////////


# 5)delete user

# user deleted successfully

# @pytest.mark.parametrize("id", [
#     30,  
# ])
# def test_user_deleted_successfully(id):
#     response = delete_user(id)

#     assert response["status"] == 201
#     assert response["message"] == "User deleted successfully"

 # id must be provided
@pytest.mark.parametrize("id", [
    ("",),  
])
def test_user_id_must_be_provided(id):
    with pytest.raises(HTTPException) as exc_info:        
        delete_user(id[0]) 
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "ID must be provided and must be an integer"

# //////////////////////////////////////////////////////////////////////////////////////////////////////

#  6) logout user


# user logout successfull

@pytest.mark.parametrize("data, authorization", [
    ({"email": "a@gmail.com"}, "Bearer valid_test_token"),
])
def test_user_logout_successfull(data, authorization):
    response = user_logout(data, authorization)
    assert response["status"] == 201
    assert response["message"] == "User logged out successfully"

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
