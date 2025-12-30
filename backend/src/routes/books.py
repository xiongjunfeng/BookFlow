from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.extensions import db
from src.models.book import Book
from src.models.user import User
from datetime import datetime

# 创建蓝图
bp = Blueprint('books', __name__)

@bp.route('/', methods=['GET'])
def get_books():
    # 获取图书列表
    books = Book.query.all()
    return jsonify({'books': [book.to_dict() for book in books]}), 200

@bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    # 获取单本图书
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': '图书不存在'}), 404
    return jsonify({'book': book.to_dict()}), 200

@bp.route('/', methods=['POST'])
@jwt_required()
def add_book():
    # 添加图书
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    # 检查权限
    if user.role != 'admin':
        return jsonify({'message': '没有权限添加图书'}), 403
    
    data = request.get_json()
    
    # 检查必填字段
    required_fields = ['book_no', 'title', 'author', 'publisher', 'publish_date', 'category', 'price', 'stock']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'message': f'{field}不能为空'}), 400
    
    # 检查图书编号是否已存在
    if Book.query.filter_by(book_no=data['book_no']).first():
        return jsonify({'message': '图书编号已存在'}), 400
    
    # 创建新图书
    try:
        publish_date = datetime.strptime(data['publish_date'], '%Y-%m-%d').date()
        book = Book(
            book_no=data['book_no'],
            title=data['title'],
            author=data['author'],
            publisher=data['publisher'],
            publish_date=publish_date,
            category=data['category'],
            price=float(data['price']),
            stock=int(data['stock']),
            cover_image=data.get('cover_image')
        )
        
        db.session.add(book)
        db.session.commit()
        return jsonify({'message': '添加图书成功', 'book': book.to_dict()}), 201
    except ValueError:
        return jsonify({'message': '出版日期格式错误，应为YYYY-MM-DD'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '添加图书失败', 'error': str(e)}), 500

@bp.route('/<int:book_id>', methods=['PUT'])
@jwt_required()
def update_book(book_id):
    # 更新图书
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    # 检查权限
    if user.role != 'admin':
        return jsonify({'message': '没有权限更新图书'}), 403
    
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': '图书不存在'}), 404
    
    data = request.get_json()
    
    try:
        if 'book_no' in data and data['book_no'] != book.book_no:
            if Book.query.filter_by(book_no=data['book_no']).first():
                return jsonify({'message': '图书编号已存在'}), 400
            book.book_no = data['book_no']
        
        if 'title' in data:
            book.title = data['title']
        if 'author' in data:
            book.author = data['author']
        if 'publisher' in data:
            book.publisher = data['publisher']
        if 'publish_date' in data:
            book.publish_date = datetime.strptime(data['publish_date'], '%Y-%m-%d').date()
        if 'category' in data:
            book.category = data['category']
        if 'price' in data:
            book.price = float(data['price'])
        if 'stock' in data:
            book.stock = int(data['stock'])
        if 'cover_image' in data:
            book.cover_image = data['cover_image']
        
        db.session.commit()
        return jsonify({'message': '更新图书成功', 'book': book.to_dict()}), 200
    except ValueError:
        return jsonify({'message': '出版日期格式错误，应为YYYY-MM-DD'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '更新图书失败', 'error': str(e)}), 500

@bp.route('/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    # 删除图书
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    # 检查权限
    if user.role != 'admin':
        return jsonify({'message': '没有权限删除图书'}), 403
    
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': '图书不存在'}), 404
    
    # 检查是否有库存
    if book.stock > 0:
        return jsonify({'message': '有库存的图书不可直接删除'}), 400
    
    try:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': '删除图书成功'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '删除图书失败', 'error': str(e)}), 500
