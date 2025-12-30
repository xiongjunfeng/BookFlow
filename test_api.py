import requests
import json

# 测试基本API连接
try:
    # 获取图书列表（无需认证）
    books_url = "http://localhost:5000/api/books/"
    books_response = requests.get(books_url)
    print("获取图书列表响应:", books_response.status_code)
    print("图书列表内容:", books_response.text)
    
    if books_response.status_code == 200:
        books_data = books_response.json()
        books = books_data.get("books", [])
        print(f"图书数量: {len(books)}")
        
        # 显示第一本书的信息（如果存在）
        if len(books) > 0:
            print("第一本书信息:", books[0])
    
    # 尝试注册一个不同的用户
    register_url = "http://localhost:5000/api/auth/register"
    register_data = {
        "username": "user123",
        "password": "password123"
    }
    
    register_response = requests.post(register_url, json=register_data)
    print("\n注册响应:", register_response.status_code)
    print("注册响应内容:", register_response.text)
    
    # 尝试登录
    login_url = "http://localhost:5000/api/auth/login"
    login_data = {
        "username": "user123",
        "password": "password123"
    }
    
    login_response = requests.post(login_url, json=login_data)
    print("\n登录响应:", login_response.status_code)
    print("登录响应内容:", login_response.text)
    
    if login_response.status_code == 200:
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 尝试借阅第一本书
        if len(books) > 0:
            book_id = books[0]["id"]
            print(f"\n尝试借阅图书ID: {book_id}")
            
            borrow_url = "http://localhost:5000/api/borrow"
            borrow_data = {"book_id": book_id}
            
            borrow_response = requests.post(borrow_url, json=borrow_data, headers=headers)
            print("借阅响应:", borrow_response.status_code)
            print("借阅响应内容:", borrow_response.text)
            
            # 获取借阅记录
            records_url = "http://localhost:5000/api/borrow/records/"
            records_response = requests.get(records_url, headers=headers)
            print("\n借阅记录响应:", records_response.status_code)
            print("借阅记录内容:", records_response.text)
        
except Exception as e:
    print("发生错误:", str(e))