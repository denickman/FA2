from typing import Optional
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()


# ✅ Используй BaseModel из Pydantic
class Book(BaseModel):
    id: Optional[int] = Field(description='Id is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=1, lt=6) # great then, less then

    model_config = {
        'json_schema_extra': {
            'example': {
                'title': 'My Book',
                'author': 'Deny Remena',
                'description': 'A very good book',
                'rating': 5,
            }
        }
    }





BOOKS = [
    Book(id=1, title="Computer Science", author="Den Y", description="A very smart book", rating=5),
    Book(id=2, title="ML", author="Alex C", description="A very good book", rating=5),
    Book(id=3, title="Swift", author="Roman R", description="A very bad book", rating=1),
    Book(id=4, title="Python", author="Nestor P", description="A very nice book", rating=4),
    Book(id=5, title="JS", author="Roman M", description="A very lousy book", rating=2),
    Book(id=6, title="DevOps", author="John C", description="A very bored book", rating=3),
]

# ✅ Добавь возвращаемый тип
@app.get('/books')
async def read_all_books():
    return BOOKS


# ✅ Типизируй параметр и добавь return
@app.post('/create-book')
async def create_book(book_request: Book):
    print("NEW BOOK CREATED:", book_request)
    BOOKS.append(generate_book_id(book_request))
    return {"message": "Book created successfully", "book": book_request}



def generate_book_id(book: Book):  # ✅ Правильное имя!

  # book.id = (BOOKS[-1].id + 1) if BOOKS else 1

    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book

