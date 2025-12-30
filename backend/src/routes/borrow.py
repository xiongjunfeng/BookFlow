from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.extensions import db
from src.models.user import User
from src.models.book import Book
from src.models.borrow_record import BorrowRecord
from datetime import datetime

# 创建蓝图
bp = Blueprint('borrow', __name__)

@bp.route('', methods=['POST'])
@jwt_required()
def borrow_book():
    # 借阅图书
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    
    # 检查必填字段
    if not data.get('book_id'):
        return jsonify({'message': '图书ID不能为空'}), 400
    
    try:
        book_id = int(data['book_id'])
    except ValueError:
        return jsonify({'message': '图书ID无效'}), 400
    
    # 获取用户和图书
    user = User.query.get(current_user_id)
    book = Book.query.get(book_id)
    
    # 检查用户角色 - 管理员不能借阅图书
    if user.role == 'admin':
        return jsonify({'message': '管理员不能借阅图书'}), 403
    
    if not book:
        return jsonify({'message': '图书不存在'}), 404
    
    # 检查图书库存
    if book.stock <= 0:
        return jsonify({'message': '图书库存不足，无法借阅'}), 400
    
    # 检查是否已借阅
    existing_record = BorrowRecord.query.filter_by(
        user_id=user.id,
        book_id=book.id,
        status='borrowed'
    ).first()
    
    if existing_record:
        return jsonify({'message': '您已借阅该图书，尚未归还'}), 400
    
    # 开始事务
    try:
        # 创建借阅记录
        borrow_record = BorrowRecord(
            user_id=user.id,
            book_id=book.id
        )
        
        # 更新图书库存
        book.stock -= 1
        
        # 保存到数据库
        db.session.add(borrow_record)
        db.session.commit()
        
        return jsonify({
            'message': '借阅成功',
            'borrow_record': borrow_record.to_dict(),
            'book': book.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '借阅失败', 'error': str(e)}), 500

@bp.route('/return/<int:record_id>', methods=['PUT'])
@jwt_required()
def return_book(record_id):
    # 归还图书
    current_user_id = int(get_jwt_identity())
    
    # 获取借阅记录
    borrow_record = BorrowRecord.query.filter_by(
        id=record_id,
        user_id=current_user_id,
        status='borrowed'
    ).first()
    
    if not borrow_record:
        return jsonify({'message': '借阅记录不存在或已归还'}), 404
    
    # 获取图书
    book = Book.query.get(borrow_record.book_id)
    if not book:
        return jsonify({'message': '图书不存在'}), 404
    
    # 开始事务
    try:
        # 更新借阅记录
        borrow_record.return_date = datetime.utcnow()
        borrow_record.status = 'returned'
        
        # 更新图书库存
        book.stock += 1
        
        # 保存到数据库
        db.session.commit()
        
        return jsonify({
            'message': '归还成功',
            'borrow_record': borrow_record.to_dict(),
            'book': book.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '归还失败', 'error': str(e)}), 500

@bp.route('/records/', methods=['GET'])
@jwt_required()
def get_borrow_records():
    # 获取用户的借阅记录
    current_user_id = int(get_jwt_identity())
    
    # 分页参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 查询借阅记录
    records = BorrowRecord.query.filter_by(user_id=current_user_id)\
    .order_by(BorrowRecord.borrow_date.desc())\
    .paginate(page=page, per_page=per_page, error_out=False)
    
    # 格式化结果
    result = {
        'records': [record.to_dict() for record in records.items],
        'total': records.total,
        'page': records.page,
        'per_page': records.per_page,
        'pages': records.pages
    }
    
    return jsonify(result), 200

@bp.route('/records/<int:record_id>', methods=['GET'])
@jwt_required()
def get_borrow_record(record_id):
    # 获取单条借阅记录
    current_user_id = int(get_jwt_identity())
    
    record = BorrowRecord.query.filter_by(
        id=record_id,
        user_id=current_user_id
    ).first()
    
    if not record:
        return jsonify({'message': '借阅记录不存在'}), 404
    
    return jsonify({'record': record.to_dict()}), 200
