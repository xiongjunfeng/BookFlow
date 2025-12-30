#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from werkzeug.security import generate_password_hash

def reset_xjf_password():
    print("=== 重置xjf用户密码 ===\n")
    
    db_path = "d:/trae_projects/BookFlow/backend/instance/bookflow.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 生成新密码的哈希值
        new_password = "123456"
        password_hash = generate_password_hash(new_password)
        
        # 更新xjf用户的密码
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (password_hash, "xjf"))
        
        if cursor.rowcount > 0:
            print(f"✅ 用户'xjf'的密码已重置为: {new_password}")
            
            # 验证更新
            cursor.execute("SELECT username, password FROM users WHERE username = ?", ("xjf",))
            user = cursor.fetchone()
            if user:
                print(f"✅ 验证更新成功")
                print(f"   用户名: {user[0]}")
                print(f"   密码哈希: {user[1][:50]}...")
            else:
                print("❌ 更新后用户不存在")
        else:
            print("❌ 用户'xjf'不存在")
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"❌ 密码重置失败: {e}")

if __name__ == "__main__":
    reset_xjf_password()