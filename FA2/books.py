from fastapi import FastAPI, Body, HTTPException

app = FastAPI()

BOOKS = [
    {'title': 'Book 1', 'author': 'Author 1', 'category': 'Science'},
    {'title': 'Book 2', 'author': ' ', 'category': 'History'},
    {'title': 'Book 3', 'author': 'Author 3', 'category': 'Math'},
    {'title': 'Book 4', 'author': 'Author 4', 'category': 'Science'},
    {'title': 'Book 5', 'author': 'Author 5', 'category': 'History'},
    {'title': 'Book 6', 'author': 'Author 2', 'category': 'Math'},
]


# 1️⃣ Все книги
@app.get("/api-endpoint")
async def read_all_books():
    return BOOKS


# 2️⃣ Любимая книга (статический маршрут)
@app.get("/books/mybook")
async def read_my_book():
    return {'book_title': 'My favorite book!'}


# 3️⃣ Фильтр по категории и/или автору (QUERY PARAMS)
@app.get("/books/")
async def read_books(category: str = None, author: str = None):
    books_to_return = []

    for book in BOOKS:
        # Если указана категория, проверяем её
        if category and book.get('category').casefold() != category.casefold():
            continue

        # Если указан автор, проверяем его
        if author and book.get('author').casefold() != author.casefold():
            continue

        # Если оба фильтра прошли (или не были указаны), добавляем книгу
        books_to_return.append(book)

    # Если ничего не нашли, возвращаем пустой список (или можешь выбросить 404)
    if not books_to_return:
        raise HTTPException(status_code=404, detail="No books found matching your criteria")

    return books_to_return


# 4️⃣ Поиск по названию книги (PATH PARAM)
@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book

    raise HTTPException(status_code=404, detail="Book not found")


# 5️⃣ Создать новую книгу
@app.post('/books/create_book')
async def create_book(new_book=Body()):
    print("NEW BOOK", new_book)
    BOOKS.append(new_book)
    return {"message": "Book created successfully", "book": new_book}


# 6️⃣ Обновить существующую книгу
@app.put('/books/update_book')
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book
            return {"message": "Book updated successfully", "book": updated_book}

    raise HTTPException(status_code=404, detail="Book not found")


# 7️⃣ Удалить книгу по названию
@app.delete('/books/delete_book/{book_title}')
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            removed_book = BOOKS.pop(i)
            return {"message": "Book deleted successfully", "book": removed_book}

    raise HTTPException(status_code=404, detail="Book not found")


'''
    Get all books from a specific author using path parameters
'''


# 8️⃣ Получить все книги конкретного автора
@app.get('/books/byauthor/{author}')
async def read_books_by_author_path(author: str):
    books_to_return = []

    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)

    if not books_to_return:
        raise HTTPException(status_code=404, detail="No books found for this author")

    return books_to_return