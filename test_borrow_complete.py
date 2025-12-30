#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

def test_complete_borrow_flow():
    base_url = "http://localhost:5000/api"
    
    print("=== 开始完整借阅流程测试 ===\n")
    
    # 1. 测试获取图书列表
    print("1. 获取图书列表...")
    books_response = requests.get(f"{base_url}/books/")
    if books_response.status_code == 200:
        books_data = books_response.json()
        books = books_data.get("books", [])
        print(f"✅ 获取图书列表成功，共 {len(books)} 本书")
        
        # 选择第一本书进行测试
        if len(books) > 0:
            test_book = books[0]
            original_stock = test_book["stock"]
            print(f"   测试图书: {test_book['title']}")
            print(f"   原始库存: {original_stock}")
            
            # 2. 注册用户
            print("\n2. 注册新用户...")
            username = f"test_user_{int(time.time())}"
            password = "password123"
            
            register_response = requests.post(f"{base_url}/auth/register", json={
                "username": username,
                "password": password
            })
            
            if register_response.status_code == 201:
                print(f"✅ 用户 {username} 注册成功")
                
                # 3. 登录用户
                print("\n3. 登录用户...")
                login_response = requests.post(f"{base_url}/auth/login", json={
                    "username": username,
                    "password": password
                })
                
                if login_response.status_code == 200:
                    login_data = login_response.json()
                    token = login_data["access_token"]
                    print(f"✅ 用户 {username} 登录成功")
                    
                    # 4. 借阅图书
                    print("\n4. 借阅图书...")
                    headers = {"Authorization": f"Bearer {token}"}
                    
                    borrow_response = requests.post(f"{base_url}/borrow", 
                        json={"book_id": test_book["id"]},
                        headers=headers
                    )
                    
                    if borrow_response.status_code == 201:
                        borrow_data = borrow_response.json()
                        print("✅ 借阅成功")
                        print(f"   借阅记录: {borrow_data}")
                        
                        # 5. 验证库存是否更新
                        print("\n5. 验证库存更新...")
                        updated_books_response = requests.get(f"{base_url}/books/")
                        if updated_books_response.status_code == 200:
                            updated_books_data = updated_books_response.json()
                            updated_books = updated_books_data.get("books", [])
                            
                            # 查找同一本书的更新后库存
                            updated_book = None
                            for book in updated_books:
                                if book["id"] == test_book["id"]:
                                    updated_book = book
                                    break
                            
                            if updated_book:
                                new_stock = updated_book["stock"]
                                print(f"   更新后库存: {new_stock}")
                                if new_stock == original_stock - 1:
                                    print("✅ 库存正确减少")
                                else:
                                    print(f"❌ 库存异常: 期望 {original_stock - 1}, 实际 {new_stock}")
                            
                            # 6. 检查借阅记录
                            print("\n6. 检查借阅记录...")
                            records_response = requests.get(f"{base_url}/borrow/records/", headers=headers)
                            if records_response.status_code == 200:
                                records_data = records_response.json()
                                records = records_data.get("records", [])
                                print(f"✅ 获取借阅记录成功，共 {len(records)} 条记录")
                                
                                # 检查是否有刚借阅的记录
                                borrowed_books = [r for r in records if r["book_id"] == test_book["id"] and not r["return_date"]]
                                if borrowed_books:
                                    print("✅ 借阅记录正确显示")
                                    print(f"   借阅记录: {borrowed_books[0]}")
                                else:
                                    print("❌ 未找到刚借阅的记录")
                            else:
                                print(f"❌ 获取借阅记录失败: {records_response.status_code}")
                                print(f"   响应: {records_response.text}")
                        
                    else:
                        print(f"❌ 借阅失败: {borrow_response.status_code}")
                        print(f"   响应: {borrow_response.text}")
                else:
                    print(f"❌ 登录失败: {login_response.status_code}")
                    print(f"   响应: {login_response.text}")
            else:
                print(f"❌ 注册失败: {register_response.status_code}")
                print(f"   响应: {register_response.text}")
        else:
            print("❌ 没有可用的图书进行测试")
    else:
        print(f"❌ 获取图书列表失败: {books_response.status_code}")
        print(f"   响应: {books_response.text}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_complete_borrow_flow()