from src.extensions import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_no = db.Column(db.String(50), nullable=False, unique=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    publish_date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    cover_image = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    borrow_records = db.relationship('BorrowRecord', backref='book', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'book_no': self.book_no,
            'title': self.title,
            'author': self.author,
            'publisher': self.publisher,
            'publish_date': self.publish_date.isoformat() if self.publish_date else None,
            'category': self.category,
            'price': self.price,
            'stock': self.stock,
            'cover_image': self.cover_image,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
