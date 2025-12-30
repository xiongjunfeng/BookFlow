#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试借阅一本xjf用户没有借阅过的书
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def main():
    print("🔍 测试借阅xjf用户未借阅过的图书")
    print("=" * 50)
    
    # 1. xjf用户登录
    print("=== 1. xjf用户登录 ===")
    login_data = {
        "username": "xjf",
        "password": "123456"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        result = response.json()
        token = result['access_token']
        user = result['user']
        print(f"✅ 登录成功: {user['username']}")
        
        # 2. 获取图书列表
        print("\n=== 2. 获取图书列表 ===")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/books/", headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            books = result['books']
            print(f"✅ 获取到 {len(books)} 本图书")
            
            # 3. 查看xjf用户的借阅记录
            print("\n=== 3. 查看xjf用户的借阅记录 ===")
            response = requests.get(f"{BASE_URL}/borrow/records/", headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                records = result['records']
                print(f"✅ xjf用户有 {len(records)} 条借阅记录")
                
                # 获取已借阅的图书ID
                borrowed_book_ids = set()
                for record in records:
                    if record['status'] != 'returned':  # 未归还的
                        borrowed_book_ids.add(record['book_id'])
                
                print(f"当前借阅的图书ID: {sorted(borrowed_book_ids)}")
                
                # 4. 找一本未借阅且有库存的书
                print("\n=== 4. 寻找可借阅的图书 ===")
                available_books = []
                for book in books:
                    if book['stock'] > 0 and book['id'] not in borrowed_book_ids:
                        available_books.append(book)
                
                if available_books:
                    test_book = available_books[0]  # 选择第一本可借阅的书
                    print(f"📚 选择测试图书: {test_book['title']} (ID: {test_book['id']}, 库存: {test_book['stock']})")
                    
                    # 5. 尝试借阅
                    print(f"\n=== 5. 借阅测试图书 ===")
                    borrow_data = {"book_id": test_book['id']}
                    response = requests.post(f"{BASE_URL}/borrow", json=borrow_data, headers=headers)
                    
                    print(f"状态码: {response.status_code}")
                    print(f"响应: {response.text}")
                    
                    if response.status_code == 201:
                        print("✅ 借阅成功!")
                        
                        # 6. 验证借阅记录
                        print("\n=== 6. 验证借阅记录更新 ===")
                        response = requests.get(f"{BASE_URL}/borrow/records/", headers=headers)
                        if response.status_code == 200:
                            result = response.json()
                            records = result['records']
                            new_records = [r for r in records if r['book_id'] == test_book['id']]
                            print(f"新增借阅记录: {len(new_records)} 条")
                            for record in new_records:
                                print(f"  - 图书ID: {record['book_id']}, 状态: {record['status']}, 日期: {record['borrow_date']}")
                        
                        # 7. 验证库存变化
                        print("\n=== 7. 验证库存变化 ===")
                        response = requests.get(f"{BASE_URL}/books/", headers=headers)
                        if response.status_code == 200:
                            result = response.json()
                            books_after = result['books']
                            updated_book = next((b for b in books_after if b['id'] == test_book['id']), None)
                            if updated_book:
                                print(f"📉 库存变化: {test_book['stock']} → {updated_book['stock']}")
                    else:
                        print(f"❌ 借阅失败")
                else:
                    print("❌ 没有找到可借阅的图书")
            else:
                print(f"❌ 获取借阅记录失败: {response.text}")
        else:
            print(f"❌ 获取图书列表失败: {response.text}")
    else:
        print(f"❌ 登录失败: {response.text}")

if __name__ == "__main__":
    main()