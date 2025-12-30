from flask import Flask
from src.extensions import db
from datetime import datetime, timedelta
import random
import string
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建Flask应用实例
app = Flask(__name__)

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'instance', 'bookflow.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db.init_app(app)

# 导入所有模型
from src.models.user import User
from src.models.book import Book
from src.models.borrow_record import BorrowRecord

# 随机生成图书编号
def generate_book_no():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# 随机生成书名
book_titles = [
    'Python编程从入门到精通', 'JavaScript高级程序设计', '数据结构与算法分析',
    '机器学习实战', '深度学习入门', '人工智能：一种现代的方法',
    '计算机网络：自顶向下方法', '操作系统概念', '数据库系统概念',
    '软件工程：实践者的研究方法', '设计模式：可复用面向对象软件的基础',
    'Effective Java', 'C++ Primer Plus', 'Head First设计模式',
    '算法导论', '重构：改善既有代码的设计', '代码整洁之道',
    '人月神话', '软技能：代码之外的生存指南', '图解HTTP',
    '图解TCP/IP', '深入理解计算机系统', 'Python Cookbook'
]

# 随机生成作者
authors = [
    '张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十',
    '陈一', '林二', '黄三', '何四', '郑五', '王六', '冯七', '陈八'
]

# 随机生成出版社
publishers = [
    '机械工业出版社', '电子工业出版社', '人民邮电出版社', '清华大学出版社',
    '北京大学出版社', '高等教育出版社', '中国电力出版社', '中国水利水电出版社'
]

# 随机生成分类
categories = [
    '计算机科学', '编程技术', '人工智能', '网络技术', '数据库',
    '软件工程', '操作系统', '数据结构', '算法', '设计模式'
]

# 生成随机日期
def random_date(start_year=2000, end_year=2025):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

# 生成随机价格
def random_price(min_price=20, max_price=150):
    return round(random.uniform(min_price, max_price), 2)

# 生成随机库存
def random_stock(min_stock=0, max_stock=50):
    return random.randint(min_stock, max_stock)

# 主函数
if __name__ == '__main__':
    with app.app_context():
        # 生成23本新图书
        for i in range(23):
            book = Book(
                book_no=generate_book_no(),
                title=book_titles[i % len(book_titles)],
                author=random.choice(authors),
                publisher=random.choice(publishers),
                publish_date=random_date(),
                category=random.choice(categories),
                price=random_price(),
                stock=random_stock()
            )
            db.session.add(book)
            print(f"生成图书 {i+1}: {book.title} - {book.author}")
        
        # 提交到数据库
        try:
            db.session.commit()
            print("成功生成23本图书并插入数据库。")
        except Exception as e:
            db.session.rollback()
            print(f"生成图书时出错: {str(e)}")
