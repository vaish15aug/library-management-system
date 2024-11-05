import pytest 
from controller.admin import createAdmin,adminLogin,updateAdmin, get_admin, admin_logout
from fastapi import HTTPException
from fastapi.testclient import TestClient
from main import app  
from schema.admin import AdminUpdate, AdminLogout

client = TestClient(app)

# create admin
# @pytest.mark.parametrize("data",[
#     ({
#         "name":"vandana", "email":"vandana@gmail.com", "password":"vaish1", "phone":"98564555","is_super":True
#     }),
# ])
# def test_create_admin(data):
    
#     admin_details = createAdmin(data)
#     assert admin_details['status'] == 201 , f"admin created => {data}"

#  check if the admin data is entered correctly
@pytest.mark.parametrize("data", [
    ({
        "email":"vaishnavi@gmail.com" , "password":"vaish1", "phone": "985641230"
    }),
])
def test_create_missing_admin_name(data):
    with pytest.raises(HTTPException) as exc_info: 
        createAdmin(data)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Name is required"


# check if the email is proper
@pytest.mark.parametrize("data", [
    ({
         "name":"vaishnavi",  "password":"vaish1", "phone":"985641230"
    }),
])
def test_create_admin_missing_email(data):
    with pytest.raises(HTTPException) as exc_info:
        createAdmin(data)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Email is required"

#  check if the password is given 
@pytest.mark.parametrize("data", [
    ({
        "name":"vaishnavi", "email":"vaishnavi@gmail.com","phone":"985641230"
    }),
])
def test_create_admin_missing_password(data):
    
    with pytest.raises(HTTPException) as exc_info:
        createAdmin(data)
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Password is required"


#  check if the name is given 
@pytest.mark.parametrize("data", [
    ({
        "email":"vaishnavi@gmail.com", "password":"vaish1", "phone":"985641230"
    }),
])
def test_create_admin_missing_name(data):

    with pytest.raises(HTTPException) as exc_info:
        createAdmin(data)   
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Name is required"


#  check if phone number is given 
@pytest.mark.parametrize("data", [
    ({
        "name":"vaishnavi", "email":"vaishnavi@gmail.com","password":"vaish1"
    }),
])
def test_create_admin_missing_phone(data):

    with pytest.raises(HTTPException) as exc_info:
        createAdmin(data)   
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Phone number is required"
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#  admin login 
def test_admin_data(test_get_admin_access_token):
    print("test_get_admin_access_token ->>",test_get_admin_access_token)


@pytest.mark.parametrize("data", [
    ({ "email":"vaishnavi@gmail.com","password":"vaish1"}),
])
def test_admin_login_success(data):
    response = adminLogin(data)  
    assert response['status'] == 200, f"Login failed => {data}"
    assert response['message'] == "Login successfull"
    assert "accessToken" in response["data"]
    assert "refreshToken" in response["data"]

#  check if email is provided
@pytest.mark.parametrize("data", [
    ({ "password":"vaish1"}),   
])
def test_admin_login_missing_email(data):
    with pytest.raises(HTTPException) as exc_info:
        adminLogin(data)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Email is required"

#  check if password is provided
@pytest.mark.parametrize("data", [
    ({ "email":"vaishnavi@gmail.com"}),
])
def test_user_login_missing_password(data):
    with pytest.raises(HTTPException) as exc_info:
        adminLogin(data)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Password is required"

# Non-existing user
@pytest.mark.parametrize("data", [
    ({"email": "nonexisting@gmail.com", "password": "wrongpassword"}),
])
def test_admin_login_admin_not_found(data):
    with pytest.raises(HTTPException) as exc_info:
        adminLogin(data)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Failed to login"


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#  admin update

@pytest.mark.parametrize("id, data", [
    ("5", {"name": "Sakshi Ulhe", "phone": "7896541200"}),
])
def test_admin_update(id, data):
    payload = {"id": id}
    request_data = AdminUpdate(**data) 
    response = updateAdmin(request_data, payload)
    
    assert response["status"] == 201
    assert response["message"] == "Admin updated successfully"

#  check only name , phone number can be updated

@pytest.mark.parametrize("id, data", [
    (5, {}),  # No valid fields provided
])
def test_admin_name_phone_can_be_updated(id, data):
    payload = {"id": id}
    with pytest.raises(HTTPException) as exc_info:
        updateAdmin(AdminUpdate(**data), payload)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Only name, phone number can be updated"


# Test for updating  name
@pytest.mark.parametrize("id, data", [
    (5, {"name": "Sakshi desh"}), 
])
def test_admin_name_updated(id, data):
    payload = {"id": id} 
    request_data = AdminUpdate(**data)  # Create an instance from data
    response = updateAdmin(request_data, payload)

    assert response["status"] == 201
    assert response["message"] == 'Admin updated successfully'

# Test for updating phone
@pytest.mark.parametrize("id, data", [
    (5, {"phone": 789600000}),  
])
def test_admin_phone_updated(id, data):
    payload = {"id": id}  
    request_data = AdminUpdate(**data)  # Create an instance from data
    response = updateAdmin(request_data, payload)

    assert response["status"] == 201
    assert response["message"] == 'Admin updated successfully'


# admin not found 
@pytest.mark.parametrize("id, data", [
    (1, {"name": "Sakshi"}), 
])
def test_admin_update_admin_not_found(id, data):
    payload = {"id": id} 
    with pytest.raises(HTTPException) as exc_info:
        request_data = AdminUpdate(**data)  
        updateAdmin(request_data, payload)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Admin not found"


# ///////////////////////////////////////////////////////////////////////////////////////////////

# get admin  
# admin found successfully


@pytest.mark.parametrize("id", [
    6,  
])
def test_user_found_successfully(id):
    response = get_admin(id)

    assert response["status"] == 200
    assert response["message"] == "Admin found successfully"
#  check if we can find admin by its id

@pytest.mark.parametrize("id", [
    (5,),  
])
def test_get_admin(id):
    response = get_admin(id[0]) 
    assert response["status"] == 200    
    assert response["data"].id == id[0]  
 
#  check if the id we provide is available or not
@pytest.mark.parametrize("id", [
    1,
])
def test_get_admin_not_found(id):
    with pytest.raises(HTTPException) as exc_info:
        get_admin(id) 
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Admin not found"


# check if the id is provieded in proper format 
@pytest.mark.parametrize("id", [
    ("five"),  
])  
def test_get_admin_invalid_id(id):
    with pytest.raises(HTTPException) as exc_info:
        get_admin(id) 
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Please provide valid id"

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////



# logout Admin

# # admin logout successfull

@pytest.mark.parametrize("data, authroization", [
    ({"email": "sakshi@gmail.com"},"Bearer valid_test_token")
])
def test_admin_logout_success(data, authroization):
    response = admin_logout(data, authroization)
    assert response["status"] == 201
    assert response["message"] == "Admin logged out successfully"


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////




