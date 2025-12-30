import requests
import json

# 登录获取token
def login_get_token():
    url = 'http://localhost:5000/api/auth/login'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'username': 'test_user',  # 假设存在的测试用户
        'password': 'password123'  # 假设的密码
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(f"Login Status Code: {response.status_code}")
        if response.status_code == 200:
            return response.json().get('access_token')
        else:
            print(f"Login Failed: {response.json()}")
            return None
    except Exception as e:
        print(f"Login Error: {str(e)}")
        return None

# 测试借阅API
def test_borrow_api(token):
    url = 'http://localhost:5000/api/borrow'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    data = {
        'book_id': 1
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(f"Borrow Status Code: {response.status_code}")
        print(f"Borrow Response Body: {response.json()}")
        return response
    except Exception as e:
        print(f"Borrow Error: {str(e)}")
        return None

# 创建测试用户
def create_test_user():
    url = 'http://localhost:5000/api/auth/register'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'username': 'test_user',
        'password': 'password123'
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(f"Create User Status Code: {response.status_code}")
        if response.status_code == 201:
            print("Test user created successfully")
            return True
        else:
            print(f"Create User Result: {response.json()}")
            # 如果用户已存在，也返回True
            if '用户名已存在' in response.json().get('message', ''):
                return True
            return False
    except Exception as e:
        print(f"Create User Error: {str(e)}")
        return False

# 获取图书列表
def get_books():
    url = 'http://localhost:5000/api/books/'
    try:
        response = requests.get(url)
        print(f"Get Books Status Code: {response.status_code}")
        if response.status_code == 200:
            books = response.json().get('books', [])
            print(f"Available Books: {books}")
            return books
        else:
            print(f"Get Books Failed: {response.json()}")
            return []
    except Exception as e:
        print(f"Get Books Error: {str(e)}")
        return []

if __name__ == "__main__":
    # 先获取图书列表，查看有哪些图书可借
    get_books()
    
    # 创建测试用户
    create_test_user()
    
    # 登录获取token
    token = login_get_token()
    if token:
        test_borrow_api(token)
