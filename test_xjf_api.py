#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def test_xjf_borrow_records():
    print("=== 测试xjf用户的借阅记录API ===\n")
    
    base_url = "http://localhost:5000/api"
    
    # 首先测试登录xjf用户
    print("1. 登录xjf用户...")
    login_response = requests.post(f"{base_url}/auth/login", json={
        "username": "xjf",
        "password": "123456"  # 假设密码
    })
    
    print(f"登录状态码: {login_response.status_code}")
    print(f"登录响应: {login_response.text}")
    
    if login_response.status_code == 200:
        login_data = login_response.json()
        token = login_data["access_token"]
        print(f"✅ 登录成功，获取到token")
        
        # 测试获取借阅记录
        print(f"\n2. 获取xjf用户的借阅记录...")
        headers = {"Authorization": f"Bearer {token}"}
        
        records_response = requests.get(f"{base_url}/borrow/records/", headers=headers)
        print(f"获取借阅记录状态码: {records_response.status_code}")
        print(f"获取借阅记录响应: {records_response.text}")
        
        if records_response.status_code == 200:
            records_data = records_response.json()
            records = records_data.get("records", [])
            print(f"✅ 获取借阅记录成功，共 {len(records)} 条记录")
            
            for record in records:
                print(f"   记录ID: {record.get('id')}, 图书ID: {record.get('book_id')}, 状态: {record.get('status')}")
        else:
            print(f"❌ 获取借阅记录失败")
        
        # 测试获取图书列表
        print(f"\n3. 获取图书列表...")
        books_response = requests.get(f"{base_url}/books/", headers=headers)
        print(f"获取图书列表状态码: {books_response.status_code}")
        
        if books_response.status_code == 200:
            books_data = books_response.json()
            books = books_data.get("books", [])
            print(f"✅ 获取图书列表成功，共 {len(books)} 本书")
            
            # 检查图书ID=13的信息
            book_13 = None
            for book in books:
                if book.get("id") == 13:
                    book_13 = book
                    break
            
            if book_13:
                print(f"✅ 找到图书ID=13: {book_13.get('title')}, 库存: {book_13.get('stock')}")
            else:
                print("❌ 未找到图书ID=13")
        else:
            print(f"❌ 获取图书列表失败")
            
        # 测试借阅图书
        print(f"\n4. 测试借阅图书ID=1...")
        borrow_response = requests.post(f"{base_url}/borrow", 
            json={"book_id": 1},
            headers=headers
        )
        print(f"借阅状态码: {borrow_response.status_code}")
        print(f"借阅响应: {borrow_response.text}")
        
    else:
        print(f"❌ 登录失败，可能密码不正确")

if __name__ == "__main__":
    test_xjf_borrow_records()