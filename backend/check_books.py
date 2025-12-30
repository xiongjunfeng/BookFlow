from app import app
from src.extensions import db
from src.models.book import Book

with app.app_context():
    book_count = Book.query.count()
    print(f'数据库中图书数量: {book_count}')
    
    books = Book.query.all()
    print('前10本图书:')
    for book in books[:10]:
        print(f'ID: {book.id}, 书名: {book.title}, 作者: {book.author}, 库存: {book.stock}')
