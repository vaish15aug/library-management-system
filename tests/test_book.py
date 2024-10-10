import pytest
from controller.book import get_book, get_all_books, search_books, createBook, update_book, delete_book
from fastapi import HTTPException
from models.book import Book
# #1) get single book by its id
# @pytest.mark.parametrize(("id"),(77,1,78))
# def test_get_book(id):
#     book_details = get_book(id)
#     assert len(book_details) > 0, f"There is no book with this id => {id}"


# #2) search a book by its name or author.
# @pytest.mark.parametrize(("search_param"),("Harper Lee","DSA"))
# def test_search_books(search_param):
#     book_details = search_books(search_param)
#     assert len(book_details) > 0, f"There is no book => {search_param}"

# @pytest.mark.parametrize(("category"),( "Drama"))
# def test_search_books_category(category):
#    book_details = search_books(category)
#    assert len(book_details) > 0, f"There is no book with this category => {category}"

# @pytest.mark.parametrize(("is_available"),("true", "false"))
# def test_search_books_is_available(is_available):
#     book_details = search_books(is_available)
#     assert len(book_details) > 0, f"There is no book available => {is_available}"

# #3) get a book list
# @pytest.mark.parametrize(("offset","limit","expected_count"),[(0, 10, 2),(0, 5, 5),(10, 5, 0)])
# def test_get_all_books(offset, limit,expected_count):
#     book_details = get_all_books(offset, limit,expected_count)
#     assert len(book_details) > 0, f"there is no book list => {offset, limit,expected_count}"


# # 4) create a book
# @pytest.mark.parametrize("data", "payload",[
#   ({"book_name": "1920000", "author":"ram", "category":"Drama" , "publish_date":" 2000-07-23", "is_available":True},
#    {"is_super": True}),
# ])
# def test_createBook(data,payload):
#     book_details = createBook("data","payload")
#     assert book_details['status'] == 201, f"book not created => {data}"

# #    4).1) missing required field
# @pytest.mark.parametrize("data", "payload",[
#     ({"author":"ram", "category":"Drama" , "publish_date":" 2000-07-23", "is_available":True},
#      {"is_super":True})
# ])
# def test_createBook_missing_field("data", "payload"):
#     book_details = createBook(data, payload)
#     assert book_details['status'] == 500, f"missing 'book_name' field => {data}"
    


# #5) update a book by its id
# @pytest.mark.parametrize("id,data, payload",[
#   (77, {"book_name": "19201", "author": "J.D. Marathon ", "category": "Drama", "publish_date": "2000-07-17"},
#    {"is_super": True}),
# ])
# def test_update_book( id,data, payload):
#     book_details = update_book(data,id, payload)
#     assert book_details['status'] == 201, f"book not updated => {data}, id:{id}"


# # 6)delete a book by its book id
# @pytest.mark.parametrize("id,payload",[(82,{"is_super": True}),])
# def test_delete_book(id,payload):
#     book_details = delete_book(id,payload)
#     assert len(book_details) > 0, f"There is no book => {id}"

# @pytest.fixture
# def valid_payload():
#     return {"is_super": True}

# @pytest.fixture
# def invalid_payload():
#     return {"is_super": False}

# @pytest.mark.parametrize("data", [
#     {"book_name": "199011", "author": "J.D. Marathon", "category": "Drama", "publish_date": "2000-07-16", "is_available": True},
# ])
# # def test_createBook_with_fixture(data, valid_payload):
# #     book_details = createBook(data, valid_payload)
# #     assert book_details['status'] == 201

# def test_createBook_unauthorized(data, invalid_payload):
#     book_details = createBook(data, invalid_payload)
#     assert book_details['status'] == 403



# Assuming Book model and a search_books function exists
# For seeding test data and setting up the database session
@pytest.fixture
def setup_books(db):
    # Seed some books into the test database
    book1 = Book(name="To Kill a Mockingbird", author="Harper Lee", category="Drama", is_available=True)
    book2 = Book(name="DSA Guide", author="John Doe", category="Educational", is_available=False)
    db.add_all([book1, book2])
    db.commit()

# Search books by name or author
@pytest.mark.parametrize("search_param", ["Harper Lee", "DSA"])
def test_search_books_by_name_or_author(search_param, setup_books):
    book_details = search_books(search_param)
    assert len(book_details) > 0, f"No books found for search parameter: {search_param}"

# Search books by category
@pytest.mark.parametrize("category", ["Drama", "Educational"])
def test_search_books_by_category(category, setup_books):
    book_details = search_books(category)
    assert len(book_details) > 0, f"No books found with category: {category}"

# Search books by availability
@pytest.mark.parametrize("is_available", [True, False])
def test_search_books_by_availability(is_available, setup_books):
    book_details = search_books(is_available)
    assert len(book_details) > 0, f"No books found for availability: {is_available}"



#  get a single book get_book (single book)
#  book id must be provided
#  


# update book
#  id must be provided 
#  if the book is available then only update data otherwise print msg book is not available


#    delete book 
# check by id 
# check if that book is available or not ,then print msg book is not available  


# search book
# (search_param: str = None, category: str = None, is_available: bool = None, payload: Dict= Depends(verifyToken))
#  search book by its name , author 
#  search book by  category
#  search book by its is_available
#  


    
# create book
# to check create book without admimn authorization 
# check if it is admin then only he can create book
# check book name is available 
#  check author name is their
#  check category is their
# check publish date is their
#  check is available status is their


# 
