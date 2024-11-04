import pytest
from controller.book import createBook,get_book, get_all_books, search_books,  update_book, delete_book
from fastapi import HTTPException
from schema.book import BookUpdate
   

#    1. create book


# create book with admin authentication

# @pytest.mark.parametrize("data", [
#     {"book_name": "python1", "author": "vaishnavi", "category": "programming", "publish_date": "2022-01-01", "is_available": True},
#    
# ])
# def test_create_book(data,test_get_admin_access_token):
#     headers = {"Authorization": f"Bearer {test_get_admin_access_token}",
#                "is_super": True }
    
#     response = createBook(data, headers)
    
#     assert response["status"] == 201
#     assert response["message"] == "Book created successfully"

# to check create book without admin authorization

@pytest.mark.parametrize("data", [
    {"book_name": "python1100", "author": "vaishnavi", "category": "programming", "publish_date": "2022-01-01", "is_available": True}, 
])
def test_create_book_without_admin_authorization(data):
    headers = {}
    with pytest.raises(HTTPException) as exc_info:
        createBook(data, headers)
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "You are not authorized to create a book"

# check book name is given
@pytest.mark.parametrize("data", [
    { "author": "vaishnavi", "category": "programming", "publish_date": "2022-01-01", "is_available": True}, 
])
def test_check_book_name_is_available(data, test_get_admin_access_token):
    headers = {"Authorization": f"Bearer {test_get_admin_access_token}",
               "is_super": True }
    
    with pytest.raises(HTTPException) as exc_info:
        createBook(data, headers)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Book name is required"



#  check author name is their
@pytest.mark.parametrize("data", [
    { "book_name": "python11", "category": "programming", "publish_date": "2022-01-01", "is_available": True},
])
def test_check_author_name_is_available(data, test_get_admin_access_token):
    headers = {"Authorization": f"Bearer {test_get_admin_access_token}",
               "is_super": True }
    
    with pytest.raises(HTTPException) as exc_info:
        createBook(data, headers)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Author name is required"


#  check category is their
@pytest.mark.parametrize("data", [
    { "book_name": "python11", "author": "vaishnavi", "publish_date": "2022-01-01", "is_available": True},
])
def test_check_category_is_available(data, test_get_admin_access_token):
    headers = {"Authorization": f"Bearer {test_get_admin_access_token}",
               "is_super": True }
    
    with pytest.raises(HTTPException) as exc_info:
        createBook(data, headers)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Category is required"

# check publish date is their
@pytest.mark.parametrize("data", [
    { "book_name": "python11", "author": "vaishnavi", "category": "programming", "is_available": True},
])
def test_check_publish_date_is_available(data, test_get_admin_access_token):
    headers = {"Authorization": f"Bearer {test_get_admin_access_token}",
               "is_super": True }
    
    with pytest.raises(HTTPException) as exc_info:
        createBook(data, headers)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Publish date is required"


#  check is available status is their
@pytest.mark.parametrize("data", [
    { "book_name": "python11", "author": "vaishnavi", "category": "programming", "publish_date": "2022-01-01"},
])
def test_check_is_available_status_is_available(data, test_get_admin_access_token):
    headers = {"Authorization": f"Bearer {test_get_admin_access_token}",
               "is_super": True }
    
    with pytest.raises(HTTPException) as exc_info:
        createBook(data, headers)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "is_available is required"

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# 2.find a book 

@pytest.mark.parametrize("id", [
    78, 
])
def test_get_existing_book(id):
    response = get_book(id)  
    assert response["status"] == 200
    assert "data" in response
    assert response["data"]["id"] == id


#  get a single book get_book (single book)
@pytest.mark.parametrize("id", [
    1,
])
def test_get_book(id):
    with pytest.raises(HTTPException) as exc_info:
        get_book(id)
    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Failed to find book"


 
#  book valid id must be provided
@pytest.mark.parametrize("id", [
    0,
]) 
def test_check_valid_id_provided(id):
    with pytest.raises(HTTPException) as exc_info:
        get_book(id)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Please provide valid id"


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# 3.get all book list

@pytest.mark.parametrize("data", [
    ({"user_id": 9}),
])
def test_get_all_books(data):
    response = get_all_books(data)      
    assert response["message"] == "Books list"
    assert "book" in response


# Pagination Functionality
@pytest.mark.parametrize("data", [
    ({"user_id": 9, "page": 1, "per_page": 10}),
    
])
def test_get_all_books_pagination(data):
    response = get_all_books(data)      
    assert response["message"] == "Books list"
    assert "book" in response


# Missing user_id in Payload
@pytest.mark.parametrize("data", [
    ({"page": 1, "per_page": 10}),
])
def test_get_all_books_missing_user_id(data):
    with pytest.raises(HTTPException) as exc_info:
        get_all_books(data)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == 'User ID is required'


# failed to find book list 
@pytest.mark.parametrize("data", [
    ({"user_id": 0}),
])
def test_get_all_books_missing_user_id(data):
    with pytest.raises(HTTPException) as exc_info:
        get_all_books(data)
    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Failed to find book list"



# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////




# @pytest.mark.parametrize("user_id", [
#     7,
# ])

# def test_get_all_books():
#     payload = {"user_id": 7}
#     response = get_all_books(payload) 
#     assert response["message"] == 'Books list'
#     assert "book" in response
#     # assert response["book"]["message"] == 'Books list'
    


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# 4. update book 
@pytest.mark.parametrize("id, update", [
    ("117", { "book_name": "pythonXYZ", "author": "vaishnavi", "category": "programming", "publish_date": "2022-01-01", "is_available": True}),
])
def test_update_book(id, update):
    payload = {"is_super": True}
    
    data = BookUpdate(**update)
    response = update_book(data, id, payload)
    assert response["status"] == 201
    assert response["message"] == "Book updated successfully"


#  if the paylod not pass then return msg you are not authorized 
@pytest.mark.parametrize("id, update", [
    ("0", { "book_name": "pythonXYZ", "author": "vaishnavi", "category": "programming", "publish_date": "2022-01-01", "is_available": True}),
]) 
def test_update_book_not_authorized(id, update):
    payload = {"is_super": False}
    
    data = BookUpdate(**update)
    with pytest.raises(HTTPException) as exc_info:
        update_book(data, id, payload)
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "You are not authorized to update a book"


#  id must be provided 
@pytest.mark.parametrize("id, update", [
    ("", { "book_name": "pythonXYZ", "author": "vaishnavi", "category": "programming", "publish_date": "2022-01-01", "is_available": True}),
])
def test_update_book_id_not_provided(id, update):
    payload = {"is_super": True}
    
    data = BookUpdate(**update)
    with pytest.raises(HTTPException) as exc_info:
        update_book(data, id, payload)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Please provide a valid id"



#  if the book is available then only update data otherwise print msg book is not available
# @pytest.mark.parametrize("id, update", [
#     ("1", { "book_name": "pythonXYZ", "author": "vaishnavi", "category": "programming", "publish_date": "2022-01-01", "is_available": False}),
# ])
# def test_update_book_not_available(id, update):
#     payload = {"is_super": True}
    
#     data = BookUpdate(**update)
#     with pytest.raises(HTTPException) as exc_info:
#         update_book(data, id, payload)
#     assert exc_info.value.status_code == 404
#     assert exc_info.value.detail == "Book not found "



# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# 5. search book

# (search_param: str = None, category: str = None, is_available: bool = None, payload: Dict= Depends(verifyToken))

@pytest.mark.parametrize("search_param, category, is_available", [
    ("python", "programming", True),
    ("vaishnavi", "programming", True),
    ("play 0.11234","Drama",True)
])
def test_search_book(search_param, category, is_available):
    payload = {"is_super": True}
    response = search_books(search_param, category, is_available, payload)
    
    assert response["status"] == 200 
    assert "data" in response  
    assert isinstance(response["data"], list)  
    assert len(response["data"]) > 0  


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#  6.  delete book 
# @pytest.mark.parametrize("id", [
#     ("107"),
# ])
# def test_delete_book(id):
#     payload = {"is_super": True}
#     response = delete_book(id, payload)
#     assert response["status"] == 201
#     assert response["message"] == "Book deleted successfully"


# check if not admin then return msg you are not authorized to delete a book
@pytest.mark.parametrize("id", [
    ("102"),
])
def test_delete_book_not_authorized(id):
    payload = {"is_super": False}
    with pytest.raises(HTTPException) as exc_info:
        delete_book(id, payload)
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "You are not authorized to delete a book"


# check if that book is available or not ,then print msg book is not available  

@pytest.mark.parametrize("id", [
    ("102"),
])
def test_delete_book_not_available(id):
    payload = {"is_super": True}
    with pytest.raises(HTTPException) as exc_info:
        delete_book(id, payload)
    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Failed to delete book "

