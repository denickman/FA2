from typing import Optional
from fastapi import FastAPI, HTTPException, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

# Field — валидация для Body (тело запроса)
# Path — валидация для Path params (параметры в пути)


# ✅ Используй BaseModel из Pydantic
class Book(BaseModel):
    id: Optional[int] = Field(description='Id is not needed on create', default=None)
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gte=1, lte=5)  # Рейтинг от 1 до 5
    published_date: int = Field(gte=1999, lte=2030)  # Год от 1999 до 2030

    model_config = {
        'json_schema_extra': {
            'example': {
                'title': 'My Book',
                'author': 'Deny Remena',
                'description': 'A very good book',
                'rating': 5,
                'published_date': 2029
            }
        }
    }


BOOKS = [
    Book(id=1, title="Computer Science", author="Den Y", description="A very smart book", rating=5, published_date=1999),
    Book(id=2, title="MLA", author="Alex C", description="A very good book", rating=5, published_date=2023),
    Book(id=3, title="Swift", author="Roman R", description="A very bad book", rating=1, published_date=2029),
    Book(id=4, title="Python", author="Nestor P", description="A very nice book", rating=4, published_date=2000),
    Book(id=5, title="JSA", author="Roman M", description="A very lousy book", rating=2, published_date=2011),
    Book(id=6, title="DevOps", author="John C", description="A very bored book", rating=3, published_date=2006),
]







# 1️⃣ Получить все книги
@app.get('/books', status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


# 2️⃣ Получить книгу по ID
@app.get('/books/{book_id}', status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book

    raise HTTPException(status_code=404, detail="Book not found")


# 3️⃣ Получить книги по рейтингу
@app.get('/books/by-rating/{rating}', status_code=status.HTTP_200_OK)
async def read_books_by_rating(rating: int = Query(gt=0, lt=6)):
    books_to_return = []

    for book in BOOKS:
        if book.rating == rating:
            books_to_return.append(book)

    if not books_to_return:
        raise HTTPException(status_code=404, detail="No books found with this rating")

    return books_to_return


# 4️⃣ Получить книги по дате публикации
@app.get('/books/by-date/{published_date}', status_code=status.HTTP_200_OK)
async def read_books_by_publish_date(published_date: int=Query(gt=1999, lt=2031)):

    books_to_return = []

    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)

    if not books_to_return:
        raise HTTPException(status_code=404, detail="No books found with this publish date")

    return books_to_return


# 5️⃣ Создать новую книгу
@app.post('/books/create-book', status_code=status.HTTP_201_CREATED)
async def create_book(book_request: Book):
    print("NEW BOOK CREATED:", book_request)
    new_book = generate_book_id(book_request)
    BOOKS.append(new_book)
    return {"message": "Book created successfully", "book": new_book}


# 6️⃣ Обновить книгу
@app.put('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_id: int, book: Book):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            book.id = book_id  # ✅ Убедись, что ID не меняется
            BOOKS[i] = book
            return {"message": "Book updated successfully", "book": book}

    raise HTTPException(status_code=404, detail="Book not found")


# 7️⃣ Удалить книгу
@app.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            removed_book = BOOKS.pop(i)
            return {"message": "Book deleted successfully", "book": removed_book}

    raise HTTPException(status_code=404, detail="Book not found")


# ✅ Генерирует автоматический ID для новой книги
def generate_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book