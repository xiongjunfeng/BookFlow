@echo off

REM 启动后端服务
echo 正在启动后端服务...
start "Backend Server" cmd /k "cd backend && python app.py"

REM 等待后端服务启动
echo 等待后端服务启动中...
timeout /t 3 /nobreak

REM 启动前端服务
echo 正在启动前端服务...
start "Frontend Server" cmd /k "cd frontend && npm run dev"

echo 系统启动完成！
echo 前端访问地址: http://localhost:3000
echo 后端API地址: http://localhost:5000

REM 等待用户输入再关闭窗口
echo 按任意键关闭此窗口...
pause > nul
