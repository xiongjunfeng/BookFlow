#!/bin/bash

# 启动后端服务
echo "正在启动后端服务..."
cd backend && python app.py &

# 等待后端服务启动
echo "等待后端服务启动中..."
sleep 3

# 启动前端服务
echo "正在启动前端服务..."
cd ../frontend && npm run dev &

echo "系统启动完成！"
echo "前端访问地址: http://localhost:3000"
echo "后端API地址: http://localhost:5000"

echo "按 Ctrl+C 停止所有服务..."

# 等待所有后台进程
wait
