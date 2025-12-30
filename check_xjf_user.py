#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from datetime import datetime
sys.path.append('backend')

from backend.app import app
from backend.src.extensions import db
from backend.src.models.user import User
from backend.src.models.borrow_record import BorrowRecord

def check_xjf_user():
    with app.app_context():
        print("=== 检查xjf用户状态 ===\n")
        print(f"检查开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # 查找xjf用户
        xjf_user = User.query.filter_by(username='xjf').first()
        
        if not xjf_user:
            print("❌ 用户'xjf'不存在")
            return
        
        print(f"✅ 找到用户'xjf':")
        print(f"   ID: {xjf_user.id}")
        print(f"   用户名: {xjf_user.username}")
        print(f"   邮箱: {xjf_user.email}")
        print(f"   是否管理员: {xjf_user.is_admin}")
        print(f"   创建时间: {xjf_user.created_at}")
        
        # 检查该用户的借阅记录
        print(f"\n=== {xjf_user.username}的借阅记录 ===")
        borrow_records = BorrowRecord.query.filter_by(user_id=xjf_user.id).order_by(BorrowRecord.created_at.desc()).all()
        
        if borrow_records:
            print(f"找到 {len(borrow_records)} 条借阅记录:")
            for i, record in enumerate(borrow_records, 1):
                print(f"   {i}. 记录ID: {record.id}")
                print(f"      图书ID: {record.book_id}")
                print(f"      借阅状态: {record.status}")
                print(f"      借阅日期: {record.borrow_date}")
                print(f"      归还日期: {record.return_date}")
                print(f"      创建时间: {record.created_at}")
                print()
        else:
            print("该用户没有任何借阅记录")
        
        # 检查是否有未归还的记录
        active_records = BorrowRecord.query.filter_by(
            user_id=xjf_user.id, 
            status='borrowed'
        ).all()
        
        print(f"=== 未归还的借阅记录 ===")
        if active_records:
            print(f"找到 {len(active_records)} 条未归还记录:")
            for record in active_records:
                print(f"   记录ID: {record.id}, 图书ID: {record.book_id}")
        else:
            print("没有未归还的记录")

if __name__ == "__main__":
    check_xjf_user()