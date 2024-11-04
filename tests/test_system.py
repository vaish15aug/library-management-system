import pytest
from controller.system import checkout_book, return_book, manage_fines, get_all_systems
from fastapi import HTTPException
from schema.system import ManageFineRequest, ReturnRequest


# # 1. checkout book 
# @pytest.mark.parametrize("data,payload", [
#     ({"user_id": "7", "book_id": "117"},{"is_super": True})
    
# ])
# def test_checkout_book(data, payload,test_get_admin_access_token):
#         headers = {"Authorization": f"Bearer {test_get_admin_access_token}","is_super": True }
#         response = checkout_book(data, headers)
#         assert response["status"] == 201
#         assert response["message"] == "Book successfully checked out"

# You are not authorized to checkout a book

@pytest.mark.parametrize("data, payload", [
    ({"user_id": "7", "book_id": "112"}, {"is_super": False})
])
def test_checkout_book_unauthorized(data, payload, test_get_admin_access_token):
    # headers = {"Authorization": f"Bearer {test_get_admin_access_token}","is_super": False }
    with pytest.raises(HTTPException) as exc_info:
        checkout_book(data, payload)
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "You are not authorized to checkout a book"

# Book is already checked out


# Book already checked out
@pytest.mark.parametrize("data, payload", [
    ({"user_id": "7", "book_id": "113"}, {"is_super": True})
])
def test_checkout_book_already_checked_out(data, payload):
    with pytest.raises(HTTPException) as exc_info:
        checkout_book(data, payload)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Book is already checked out"




# Book not found

@pytest.mark.parametrize("data", [
    ({"user_id": "7", "book_id": "1"})
])
def test_checkout_book_not_found(data, test_get_admin_access_token):
    headers = {"Authorization": f"Bearer {test_get_admin_access_token}", "is_super": True}
    with pytest.raises(HTTPException) as exc_info:  
        checkout_book(data, headers)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Book not found"


# User not found

@pytest.mark.parametrize("data, payload", [
    ({"user_id": "1", "book_id": "117"}, {"is_super": True})
])
def test_checkout_user_not_found(data, payload):
    with pytest.raises(HTTPException) as exc_info:
        checkout_book(data, payload)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "User not found"







# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# 2. return book

# returned book successfully

# @pytest.mark.parametrize("data, payload", [
#     ({"id": 34}, {"is_super": True}) 
# ])
# def test_return_book_success(data, payload, test_get_admin_access_token):
#     headers = {"Authorization": f"Bearer {test_get_admin_access_token}", "is_super": True}
#     response = return_book(data, headers)

#     assert response["status"] == 201
#     assert response["message"] == "Book successfully returned"


# you are not authorized to return book
@pytest.mark.parametrize("data, payload", [
    ({"id": 32}, {"is_super": False})
])
def test_return_book_unauthorized(data, payload, test_get_admin_access_token):
    headers = {"Authorization": f"Bearer {test_get_admin_access_token}","is_super": False }
    with pytest.raises(HTTPException) as exc_info:
        return_book(data, payload)
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "You are not authorized to return a book"


# Book already returned
@pytest.mark.parametrize("data, payload", [
    ({"id": 32}, {"is_super": True})
])
def test_return_book_not_found(data,payload, test_get_admin_access_token):
    headers = {"Authorization": f"Bearer {test_get_admin_access_token}", "is_super": True}
    with pytest.raises(HTTPException) as exc_info:
        return_book(data, headers)
    assert exc_info.value.status_code == 404

    assert exc_info.value.detail == "Book already returned"

# # checkout record not found
@pytest.mark.parametrize("data, payload", [
    ({"id": 0}, {"is_super": True})
])
def test_return_book_record_not_found(data, payload, test_get_admin_access_token):
    headers = {"Authorization": f"Bearer {test_get_admin_access_token}", "is_super": True}
    with pytest.raises(HTTPException) as exc_info:
        return_book(data, headers)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Checkout record not found"


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# #  3. manage fine
# Fine managed successfully
# @pytest.mark.parametrize("data, payload", [
#     ({"book_id": 119,"user_id": 7, "fine": "300"}, {"is_super": True})
    
# ])
# def test_manage_fine_success(data, payload, test_get_admin_access_token):
#     headers = {"Authorization": f"Bearer {test_get_admin_access_token}", "is_super": True}
#     request_data = ManageFineRequest(**data)

#     response = manage_fines(request_data,headers)
    
#     assert response["status"] == 201
#     assert response["message"] == "Fine managed successfully"



# you are not authorized to manage fine
@pytest.mark.parametrize("data, payload", [
    ({"book_id": 59,"user_id": 5, "fine": "200"}, {"is_super": False})
])
def test_manage_fine_unauthorized(data, payload, test_get_admin_access_token):
    headers = {"Authorization": f"Bearer {test_get_admin_access_token}","is_super": False }    
    with pytest.raises(HTTPException) as exc_info:
        manage_fines(data, payload) 
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "You are not authorized to manage fine"

# user_id must be an integer

@pytest.mark.parametrize("data, payload", [
    ({"book_id": 59,"user_id": "7", "fine": "200"}, {"is_super": True})
])
def test_manage_fine_user_id_not_integer(data, payload, test_get_admin_access_token):
    headers = {"Authorization": f"Bearer {test_get_admin_access_token}", "is_super": True}
    with pytest.raises(HTTPException) as exc_info:
        manage_fines(data, headers)
    assert exc_info.value.status_code == 422
    assert exc_info.value.detail == "user_id must be an integer"

# book_id must be an integer

@pytest.mark.parametrize("data, payload", [
    ({"book_id": "59","user_id": 7, "fine": "200"}, {"is_super": True})
])
def test_manage_fine_book_id_not_integer(data, payload, test_get_admin_access_token):
    headers = {"Authorization": f"Bearer {test_get_admin_access_token}", "is_super": True}
    with pytest.raises(HTTPException) as exc_info:    
        manage_fines(data, headers)
    assert exc_info.value.status_code == 422
    assert exc_info.value.detail == "book_id must be an integer"


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#  4 get all system data

# get all system list
@pytest.mark.parametrize("offset, limit, payload", [
    (0, 10, {"is_super": True})
])
def test_get_all_systems_success(offset, limit, payload, test_get_admin_access_token):
    headers = {"Authorization": f"Bearer {test_get_admin_access_token}", "is_super": True}
    response = get_all_systems(offset=offset, limit=limit, payload=payload)
    assert response["status"] == 201    
    assert response["message"] == "System list"

# you are not authorized to get system list
@pytest.mark.parametrize("offset, limit, payload", [
    (0, 10, {"is_super": False})
])
def test_get_all_systems_unauthorized(offset, limit, payload, test_get_admin_access_token):
    headers = {"Authorization": f"Bearer {test_get_admin_access_token}", "is_super": False}
    with pytest.raises(HTTPException) as exc_info:
        get_all_systems(offset=offset, limit=limit, payload=payload)
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "You are not authorized to get system list"


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
