from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.extensions import db
from src.models.user import User

# 创建蓝图
bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # 检查必填字段
    if not data.get('username') or not data.get('password'):
        return jsonify({'message': '用户名和密码不能为空'}), 400
    
    # 检查用户名是否已存在
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': '用户名已存在'}), 400
    
    # 创建新用户
    user = User(
        username=data['username'],
        email=data.get('email'),
        phone=data.get('phone'),
        role=data.get('role', 'user')
    )
    user.set_password(data['password'])
    
    try:
        db.session.add(user)
        db.session.commit()
        print(f"用户注册成功: {user.username} (ID: {user.id})")
        return jsonify({'message': '注册成功', 'user': user.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        print(f"用户注册失败: {str(e)}")
        return jsonify({'message': '注册失败', 'error': str(e)}), 500

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # 检查必填字段
    if not data.get('username') or not data.get('password'):
        return jsonify({'message': '用户名和密码不能为空'}), 400
    
    # 查找用户
    user = User.query.filter_by(username=data['username']).first()
    
    # 验证用户和密码
    if not user or not user.check_password(data['password']):
        return jsonify({'message': '用户名或密码错误'}), 401
    
    # 创建访问令牌
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        'message': '登录成功',
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

@bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': '用户不存在'}), 404
    
    return jsonify({'user': user.to_dict()}), 200
