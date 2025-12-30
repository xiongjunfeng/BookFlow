from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 创建Flask应用
app = Flask(__name__)

# 配置应用
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

# 配置数据库，使用绝对路径
db_path = os.path.join(app.root_path, 'instance', 'bookflow.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

print(f"数据库路径: {db_path}")

# 初始化CORS
CORS(app)

# 导入扩展
from src.extensions import db, jwt

# 初始化扩展
with app.app_context():
    db.init_app(app)
    jwt.init_app(app)

# 导入路由
from src.routes import auth, books, borrow

# 注册蓝图
app.register_blueprint(auth.bp, url_prefix='/api/auth')
app.register_blueprint(books.bp, url_prefix='/api/books')
app.register_blueprint(borrow.bp, url_prefix='/api/borrow')

if __name__ == '__main__':
    # 创建数据库表
    with app.app_context():
        # 导入模型
        from src.models.user import User
        from src.models.book import Book
        from src.models.borrow_record import BorrowRecord
        db.create_all()
    app.run(debug=True)
