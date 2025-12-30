#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime

def check_xjf_user_direct():
    print("=== 直接查询数据库检查xjf用户 ===\n")
    
    db_path = "d:/trae_projects/BookFlow/backend/instance/bookflow.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 查找xjf用户
        print("1. 查找用户'xjf':")
        cursor.execute("SELECT * FROM users WHERE username = ?", ('xjf',))
        xjf_user = cursor.fetchone()
        
        if not xjf_user:
            print("❌ 用户'xjf'不存在")
            return
        
        # 获取列名
        cursor.execute("PRAGMA table_info(users)")
        user_columns = [col[1] for col in cursor.fetchall()]
        
        print(f"✅ 找到用户'xjf':")
        for i, value in enumerate(xjf_user):
            print(f"   {user_columns[i]}: {value}")
        
        user_id = xjf_user[0]  # ID是第一个字段
        
        # 查找该用户的借阅记录
        print(f"\n2. 查找用户'{xjf_user[1]}'的借阅记录:")
        cursor.execute("SELECT * FROM borrow_records WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
        borrow_records = cursor.fetchall()
        
        if borrow_records:
            cursor.execute("PRAGMA table_info(borrow_records)")
            borrow_columns = [col[1] for col in cursor.fetchall()]
            
            print(f"找到 {len(borrow_records)} 条借阅记录:")
            for i, record in enumerate(borrow_records, 1):
                print(f"   记录 {i}:")
                for j, value in enumerate(record):
                    print(f"      {borrow_columns[j]}: {value}")
                print()
        else:
            print("该用户没有任何借阅记录")
        
        # 检查未归还的记录
        print(f"3. 查找未归还的借阅记录:")
        cursor.execute("SELECT * FROM borrow_records WHERE user_id = ? AND status = 'borrowed'", (user_id,))
        active_records = cursor.fetchall()
        
        if active_records:
            print(f"找到 {len(active_records)} 条未归还记录:")
            for record in active_records:
                print(f"   记录ID: {record[0]}, 图书ID: {record[2]}")
        else:
            print("没有未归还的记录")
        
        # 检查所有用户（用于比较）
        print(f"\n4. 数据库中的所有用户:")
        cursor.execute("SELECT id, username, email, is_admin FROM users")
        all_users = cursor.fetchall()
        
        print(f"总共有 {len(all_users)} 个用户:")
        for user in all_users:
            print(f"   ID: {user[0]}, 用户名: {user[1]}, 管理员: {user[3]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ 查询失败: {e}")

if __name__ == "__main__":
    check_xjf_user_direct()