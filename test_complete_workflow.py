#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的借阅流程测试
测试从登录到借阅到查看借阅列表的完整流程
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000/api"

def test_login(username, password):
    """登录测试"""
    print(f"\n=== 测试用户登录: {username} ===")
    
    data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=data)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            token = result.get('access_token')
            user = result.get('user')
            
            print(f"登录成功!")
            print(f"用户: {user}")
            print(f"Token: {token[:20]}...")
            
            return token, user
        else:
            print(f"登录失败: {response.text}")
            return None, None
            
    except Exception as e:
        print(f"登录请求失败: {e}")
        return None, None

def test_get_books(token):
    """获取图书列表"""
    print(f"\n=== 获取图书列表 ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/books/", headers=headers)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            books = result.get('books', [])
            print(f"获取到 {len(books)} 本图书")
            
            # 显示前几本书的信息
            for i, book in enumerate(books[:3]):
                print(f"  {i+1}. {book['title']} - 库存: {book['stock']}")
            
            return books
        else:
            print(f"获取图书列表失败: {response.text}")
            return []
            
    except Exception as e:
        print(f"获取图书列表请求失败: {e}")
        return []

def test_borrow_book(token, book_id):
    """借阅图书"""
    print(f"\n=== 借阅图书 ID: {book_id} ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {"book_id": book_id}
    
    try:
        response = requests.post(f"{BASE_URL}/borrow", json=data, headers=headers)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"借阅成功: {result}")
            return True
        else:
            print(f"借阅失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"借阅请求失败: {e}")
        return False

def test_get_borrow_records(token):
    """获取借阅记录"""
    print(f"\n=== 获取借阅记录 ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/borrow/records/", headers=headers)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            records = result.get('records', [])
            print(f"获取到 {len(records)} 条借阅记录")
            
            # 显示最近的借阅记录
            for record in records[:3]:
                print(f"  图书ID: {record['book_id']}, 状态: {record['status']}, 日期: {record['borrow_date']}")
            
            return records
        else:
            print(f"获取借阅记录失败: {response.text}")
            return []
            
    except Exception as e:
        print(f"获取借阅记录请求失败: {e}")
        return []

def main():
    """主测试流程"""
    print("🚀 开始完整借阅流程测试")
    print("=" * 50)
    
    # 测试用户（可以修改为其他用户）
    test_users = [
        {"username": "user1", "password": "123456"},
        {"username": "xjf", "password": "123456"}
    ]
    
    for user_info in test_users:
        print(f"\n🔍 测试用户: {user_info['username']}")
        
        # 1. 登录
        token, user = test_login(user_info['username'], user_info['password'])
        if not token:
            print(f"❌ 用户 {user_info['username']} 登录失败，跳过后续测试")
            continue
        
        # 检查用户角色
        if user.get('role') == 'admin':
            print(f"⚠️  用户 {user_info['username']} 是管理员，跳过借阅测试")
            continue
        
        # 2. 获取图书列表
        books = test_get_books(token)
        if not books:
            print(f"❌ 获取图书列表失败")
            continue
        
        # 3. 尝试借阅第一本有库存的书
        borrowable_book = None
        for book in books:
            if book['stock'] > 0:
                borrowable_book = book
                break
        
        if not borrowable_book:
            print(f"❌ 没有可借阅的图书")
            continue
        
        print(f"📚 选择借阅: {borrowable_book['title']} (库存: {borrowable_book['stock']})")
        
        # 4. 借阅图书
        success = test_borrow_book(token, borrowable_book['id'])
        if not success:
            print(f"❌ 借阅失败")
            continue
        
        # 等待一秒让数据更新
        time.sleep(1)
        
        # 5. 获取借阅记录验证
        records = test_get_borrow_records(token)
        print(f"✅ 借阅流程测试完成")
        print("=" * 50)
        
        # 只测试第一个有效用户
        break

if __name__ == "__main__":
    main()