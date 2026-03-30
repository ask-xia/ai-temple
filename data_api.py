#!/usr/bin/env python3
"""
AI神庙数据API服务
提供真实数据：天气、新闻、股票、搜索
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import json
import os

app = Flask(__name__)
CORS(app)  # 允许跨域

SKILLS_DIR = "/Users/x/.openclaw/workspace/skills"

def run_skill(skill_name, *args):
    """运行skill并返回结果"""
    skill_path = os.path.join(SKILLS_DIR, skill_name)
    if not os.path.exists(skill_path):
        return {"error": f"Skill {skill_name} not found"}
    
    try:
        # 读取SKILL.md找到运行方式
        readme = os.path.join(skill_path, "SKILL.md")
        if os.path.exists(readme):
            with open(readme, 'r') as f:
                content = f.read()
                # 这里简化处理，实际应该解析SKILL.md
                pass
        
        # 尝试直接运行skill的main脚本
        main_script = os.path.join(skill_path, "main.py")
        if os.path.exists(main_script):
            result = subprocess.run(
                ["python3", main_script] + list(args),
                capture_output=True,
                text=True,
                timeout=30
            )
            return {"output": result.stdout, "error": result.stderr}
        
        return {"error": "No main script found"}
    except Exception as e:
        return {"error": str(e)}

@app.route('/api/weather', methods=['GET'])
def get_weather():
    """获取天气数据"""
    city = request.args.get('city', 'Beijing')
    # 使用wttr.in API
    import urllib.request
    try:
        url = f"https://wttr.in/{city}?format=j1"
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            return jsonify({
                "city": city,
                "temp": data['current_condition'][0]['temp_C'],
                "condition": data['current_condition'][0]['weatherDesc'][0]['value'],
                "humidity": data['current_condition'][0]['humidity'],
                "wind": data['current_condition'][0]['windspeedKmph']
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/news', methods=['GET'])
def get_news():
    """获取科技新闻"""
    import urllib.request
    try:
        # 使用NewsAPI的免费端点或其他RSS源
        # 这里使用一个公开的科技新闻RSS转JSON服务
        url = "https://api.rss2json.com/v1/api.json?rss_url=https://feeds.feedburner.com/TechCrunch/"
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            items = data.get('items', [])[:5]
            return jsonify({
                "items": [{"title": i['title'], "link": i['link'], "date": i['pubDate']} for i in items]
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stock', methods=['GET'])
def get_stock():
    """获取股票数据（使用新浪财经API）"""
    code = request.args.get('code', 'sh000001')  # 默认上证指数
    import urllib.request
    try:
        # 新浪财经API
        url = f"https://hq.sinajs.cn/list={code}"
        req = urllib.request.Request(url, headers={'Referer': 'https://finance.sina.com.cn'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read().decode('gb2312')
            # 解析数据
            if 'var hq_str_' in data:
                parts = data.split('"')[1].split(',')
                if len(parts) > 3:
                    return jsonify({
                        "code": code,
                        "name": parts[0],
                        "price": parts[3],
                        "change": round(float(parts[3]) - float(parts[2]), 2) if len(parts) > 2 else 0,
                        "change_percent": round((float(parts[3]) - float(parts[2])) / float(parts[2]) * 100, 2) if len(parts) > 2 and float(parts[2]) > 0 else 0
                    })
            return jsonify({"error": "Invalid data"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/search', methods=['GET'])
def search():
    """搜索功能"""
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "Query required"}), 400
    
    # 返回搜索建议
    return jsonify({
        "query": query,
        "suggestions": [
            f"{query} 最新新闻",
            f"{query} 股票行情",
            f"{query} 技术分析",
            f"{query} 相关公司"
        ]
    })

@app.route('/api/papers', methods=['GET'])
def get_papers():
    """获取AI论文（arXiv）"""
    query = request.args.get('q', 'artificial intelligence')
    import urllib.request
    try:
        url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=5"
        with urllib.request.urlopen(url, timeout=10) as response:
            import xml.etree.ElementTree as ET
            data = response.read().decode()
            root = ET.fromstring(data)
            
            papers = []
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            for entry in root.findall('atom:entry', ns):
                title = entry.find('atom:title', ns).text if entry.find('atom:title', ns) is not None else ''
                summary = entry.find('atom:summary', ns).text[:200] + '...' if entry.find('atom:summary', ns) is not None else ''
                papers.append({"title": title, "summary": summary})
            
            return jsonify({"papers": papers})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/market', methods=['GET'])
def get_market():
    """获取市场概览"""
    import urllib.request
    try:
        # 获取多个指数
        indices = [
            {"name": "上证指数", "code": "sh000001"},
            {"name": "深证成指", "code": "sz399001"},
            {"name": "创业板指", "code": "sz399006"}
        ]
        
        result = []
        for idx in indices:
            url = f"https://hq.sinajs.cn/list={idx['code']}"
            req = urllib.request.Request(url, headers={'Referer': 'https://finance.sina.com.cn'})
            try:
                with urllib.request.urlopen(req, timeout=5) as response:
                    data = response.read().decode('gb2312')
                    if 'var hq_str_' in data:
                        parts = data.split('"')[1].split(',')
                        if len(parts) > 3:
                            result.append({
                                "name": idx['name'],
                                "price": parts[3],
                                "change": round(float(parts[3]) - float(parts[2]), 2),
                                "change_percent": round((float(parts[3]) - float(parts[2])) / float(parts[2]) * 100, 2) if float(parts[2]) > 0 else 0
                            })
            except:
                pass
        
        return jsonify({"indices": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({"status": "ok", "service": "AI神庙数据API"})

if __name__ == '__main__':
    print("🚀 AI神庙数据API服务启动")
    print("📡 http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)