# BookFlow 图书管理系统

一个基于 Vue 3 和 Flask 的现代化图书管理系统，支持图书借阅、用户管理、库存跟踪等功能。

## ✨ 功能特性

### 👥 用户管理
- **用户注册与登录**：支持邮箱注册，JWT token 认证
- **角色权限管理**：管理员和普通用户角色
- **用户信息显示**：登录后显示当前用户名

### 📚 图书管理
- **图书列表**：分页显示所有图书信息
- **图书搜索**：快速查找所需图书
- **库存管理**：实时显示图书库存数量

### 📖 借阅功能
- **在线借阅**：一键借阅图书，自动更新库存
- **借阅记录**：查看个人借阅历史
- **图书归还**：支持在线归还功能
- **状态跟踪**：实时显示借阅状态（借阅中/已归还）

### 🔧 系统管理
- **启动脚本**：一键启动前端和后端服务
- **跨平台支持**：Windows/Linux/macOS
- **数据持久化**：SQLite 数据库存储

## 🚀 快速开始

### 系统要求
- Node.js 16+ 
- Python 3.8+
- 现代浏览器

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd BookFlow
   ```

2. **安装后端依赖**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **安装前端依赖**
   ```bash
   cd frontend
   npm install
   ```

4. **启动系统**
   
   **Windows:**
   ```bash
   start_system.bat
   ```
   
   **Linux/macOS:**
   ```bash
   chmod +x start_system.sh
   ./start_system.sh
   ```

5. **访问系统**
   - 前端地址：http://localhost:5173
   - 后端API：http://localhost:5000

## 📖 使用指南

### 管理员登录
- **用户名**: `admin`
- **密码**: `admin123`
- **功能**: 管理图书、查看所有借阅记录、用户管理

### 普通用户注册
1. 点击"注册"链接
2. 填写邮箱和密码
3. 验证后即可登录使用

### 借阅流程
1. **登录系统**
2. **浏览图书列表**
3. **选择图书点击"借阅"**
4. **查看"我的借阅"确认记录**
5. **点击"归还"按钮还书**

## 🛠️ 技术架构

### 前端技术栈
- **Vue 3** - 渐进式 JavaScript 框架
- **Vike** - Vue SSR 框架
- **Vite** - 现代化构建工具
- **Element Plus** - Vue 3 UI 组件库
- **TypeScript** - 类型安全
- **Axios** - HTTP 客户端

### 后端技术栈
- **Flask** - 轻量级 Web 框架
- **Flask-JWT-Extended** - JWT 认证
- **SQLAlchemy** - ORM 数据库操作
- **SQLite** - 轻量级数据库
- **Werkzeug** - 密码哈希

### 项目结构
```
BookFlow/
├── backend/                 # Flask 后端
│   ├── src/
│   │   ├── app.py          # 应用入口
│   │   ├── models/         # 数据模型
│   │   ├── routes/         # API 路由
│   │   └── extensions/     # 扩展配置
│   ├── requirements.txt    # Python 依赖
│   └── ...
├── frontend/               # Vue 前端
│   ├── pages/             # 页面组件
│   ├── components/        # 通用组件
│   ├── package.json       # Node.js 依赖
│   └── ...
├── start_system.bat       # Windows 启动脚本
├── start_system.sh        # Linux/macOS 启动脚本
└── README.md             # 项目文档
```

## 🔧 开发指南

### API 接口

#### 认证相关
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/register` - 用户注册
- `GET /api/auth/me` - 获取当前用户信息

#### 图书管理
- `GET /api/books/` - 获取图书列表
- `GET /api/books/<id>` - 获取图书详情
- `POST /api/books` - 创建图书（管理员）
- `PUT /api/books/<id>` - 更新图书（管理员）

#### 借阅管理
- `POST /api/borrow/` - 借阅图书
- `POST /api/borrow/<id>/return` - 归还图书
- `GET /api/borrow/records/` - 获取借阅记录

### 数据库模型

#### 用户表 (users)
- `id`: 主键
- `username`: 用户名
- `email`: 邮箱
- `password`: 密码哈希
- `role`: 角色（admin/user）
- `created_at`: 创建时间

#### 图书表 (books)
- `id`: 主键
- `title`: 书名
- `author`: 作者
- `isbn`: ISBN
- `stock`: 库存数量
- `created_at`: 创建时间

#### 借阅记录表 (borrow_records)
- `id`: 主键
- `user_id`: 用户ID（外键）
- `book_id`: 图书ID（外键）
- `borrow_date`: 借阅日期
- `return_date`: 归还日期
- `status`: 状态（borrowed/returned）

## 🐛 故障排除

### 常见问题

1. **端口被占用**
   - 检查 5000 和 5173 端口是否被其他程序占用
   - 关闭冲突程序或修改端口配置

2. **数据库连接失败**
   - 确保 backend 目录下存在 database.db 文件
   - 检查 SQLite 文件权限

3. **前端无法访问后端**
   - 确认后端服务已启动
   - 检查 CORS 配置是否正确

4. **登录失败**
   - 验证用户名和密码是否正确
   - 检查 JWT token 是否过期

### 日志查看
- **后端日志**: 控制台输出
- **前端日志**: 浏览器开发者工具 Console
- **API 调试**: 浏览器开发者工具 Network

## 📄 许可证

本项目采用 MIT 许可证。

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来改进项目。

### 开发流程
1. Fork 项目
2. 创建功能分支
3. 提交变更
4. 推送到分支
5. 创建 Pull Request

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 GitHub Issue
- 发送邮件至项目维护者

---

**BookFlow** - 让图书管理更简单 📚✨