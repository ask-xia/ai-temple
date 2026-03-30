# AI神庙 - 部署指南

## 📁 项目结构

```
ai-temple/
├── index.html          # 首页 - 四站导航
├── shared/
│   └── styles.css      # 统一样式系统
├── data-center/
│   └── index.html      # 数据中心
├── tiantian/
│   └── index.html      # 天庭 - 资产管理
├── council/
│   └── index.html      # 长老会 - 治理审批
├── dojo/
│   └── index.html      # 道场 - 训练测试
└── backend/
    └── app.py          # FastAPI后端 (四站互联API)
```

## 🚀 部署方式

### 方式1: Netlify Drag & Drop

1. 打开 https://app.netlify.com/drop
2. 直接拖拽 `ai-temple` 文件夹到网页
3. 等待部署完成，获取URL

### 方式2: GitHub + Netlify

1. 创建GitHub仓库
2. 上传代码
3. 连接Netlify自动部署

### 方式3: 本地预览

```bash
cd ai-temple
python3 -m http.server 8080
# 访问 http://localhost:8080
```

## ⚙️ 后端启动

```bash
cd ai-temple/backend
pip3 install fastapi uvicorn
python3 -m uvicorn app:app --host 0.0.0.0 --port 8000
```

API文档: http://localhost:8000/docs

## 🔗 四站互联

根据文档4和文档5设计的四站互联架构：

```
数据中心 ──┐
           │
           ▼
 天庭 ─────┼──── 长老会
           │
           ▼
         道场
```

## 📊 功能模块

### 数据中心
- 数据采集、清洗、转换
- 分析引擎
- 报表生成
- 数据共享API

### 天庭
- 城投资产管理
- 地产资产管理
- 非标资产管理
- VaR风险计算
- 压力测试

### 长老会
- AI晋升体系 (炼气期→筑基期→金丹期→元婴期→化神期→大乘期)
- 策略审批
- 权限管理
- 审计日志

### 道场
- 模型训练
- 策略回测
- 模拟交易
- 绩效评估

## 📝 下一步

根据文档4要求：
1. 完善Docker Compose配置
2. 配置MySQL、Redis、MongoDB
3. 实现真实的数据存储
4. 添加Swagger API文档
5. 配置SSL证书

根据文档5要求：
1. 实现AI贡献度追踪
2. 自动晋升机制
3. 跨站调用API
4. 数据同步机制
