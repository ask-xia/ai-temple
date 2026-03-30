#!/bin/bash
echo "🏛️ AI 神庙网站启动中..."
echo ""

# 检测可用的服务器
if command -v python3 &> /dev/null; then
    echo "使用 Python HTTP 服务器..."
    python3 -m http.server 8080 &
    PID=$!
elif command -v npx &> /dev/null; then
    echo "使用 Node.js http-server..."
    npx http-server -p 8080 &
    PID=$!
elif command -v php &> /dev/null; then
    echo "使用 PHP 内置服务器..."
    php -S localhost:8080 &
    PID=$!
else
    echo "❌ 未找到可用的 HTTP 服务器"
    echo "请安装 Python3、Node.js 或 PHP"
    exit 1
fi

echo ""
echo "✅ 服务器已启动!"
echo "📍 本地地址: http://localhost:8080"
echo "🛑 按 Ctrl+C 停止"
echo ""

# 尝试自动打开浏览器
if command -v open &> /dev/null; then
    sleep 1 && open http://localhost:8080
elif command -v xdg-open &> /dev/null; then
    sleep 1 && xdg-open http://localhost:8080
fi

wait $PID
