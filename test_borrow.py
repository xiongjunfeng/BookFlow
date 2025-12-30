import requests
import json
import time

# 注册新用户
register_url = "http://localhost:5000/api/auth/register"
register_data = {
    "username": "testuser",
    "password": "password"
}

try:
    # 注册用户
    register_response = requests.post(register_url, json=register_data)
    print("注册响应:", register_response.status_code)
    print("注册响应内容:", register_response.text)
    
    # 登录
    login_url = "http://localhost:5000/api/auth/login"
    login_data = {
        "username": "testuser",
        "password": "password"
    }
    
    login_response = requests.post(login_url, json=login_data)
    print("登录响应:", login_response.status_code)
    print("登录响应内容:", login_response.text)
    
    if login_response.status_code == 200:
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 获取图书列表
        books_url = "http://localhost:5000/api/books/"
        books_response = requests.get(books_url, headers=headers)
        print("获取图书列表响应:", books_response.status_code)
        print("图书列表:", books_response.text)
        
        if books_response.status_code == 200:
            books_data = books_response.json()
            books = books_data["books"]
            
            if len(books) > 0:
                # 尝试借阅第一本书
                book_id = books[0]["id"]
                print(f"尝试借阅图书ID: {book_id}")
                
                borrow_url = "http://localhost:5000/api/borrow"
                borrow_data = {"book_id": book_id}
                
                borrow_response = requests.post(borrow_url, json=borrow_data, headers=headers)
                print("借阅响应:", borrow_response.status_code)
                print("借阅响应内容:", borrow_response.text)
                
                if borrow_response.status_code == 201:
                    print("借阅成功!")
                    
                    # 再次获取图书列表，检查库存是否变化
                    time.sleep(1)  # 等待数据库更新
                    books_response = requests.get(books_url, headers=headers)
                    updated_books = books_response.json()["books"]
                    
                    print("更新后的图书列表:")
                    for book in updated_books:
                        if book["id"] == book_id:
                            print(f"图书ID: {book['id']}, 书名: {book['title']}, 库存: {book['stock']}")
                    
                    # 获取借阅记录
                    records_url = "http://localhost:5000/api/borrow/records/"
                    records_response = requests.get(records_url, headers=headers)
                    print("借阅记录响应:", records_response.status_code)
                    print("借阅记录内容:", records_response.text)
                else:
                    print("借阅失败!")
            else:
                print("没有图书可供借阅!")
        else:
            print("获取图书列表失败!")
    else:
        print("登录失败!")
        
except Exception as e:
    print("发生错误:", str(e))