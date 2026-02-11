# 🤖 Smart Contract AI Assistant

**Web3 风格的智能合约 AI 问答助手** —— 一个包含现代化前端界面与高性能后端 API 的完整应用，为智能合约开发者提供实时、专业的代码生成、安全分析与技术问答。

![项目结构](https://img.shields.io/badge/结构-前后端分离-blue)
![Python版本](https://img.shields.io/badge/Python-3.8+-green)
![Flask版本](https://img.shields.io/badge/Flask-2.3.3-lightgrey)
![前端技术](https://img.shields.io/badge/前端-HTML/CSS/JS-yellow)

## ✨ 功能特性

### 🎨 **前端界面**
- **Web3 科技风格**：深色主题、霓虹渐变、几何网格、玻璃拟态效果
- **双页面设计**：品牌门户主页 + 功能完整助手交互页
- **响应式布局**：完美适配桌面与移动设备
- **实时交互**：对话式界面，支持代码高亮与格式渲染

### ⚙️ **核心功能**
- **智能问答**：专业智能合约问题解答
- **代码生成**：根据描述生成 Solidity 代码片段
- **安全分析**：识别常见漏洞并提供修复建议
- **技术指导**：DeFi 机制、Gas 优化、升级模式等深度解析

### 🔧 **技术特性**
- **前后端分离**：清晰架构，独立部署
- **OpenAI 兼容**：支持最新 OpenAI 1.x API
- **API 密钥保护**：安全的接口访问控制
- **实时状态追踪**：Token 用量、模型信息、响应来源

## 📁 项目结构

```bash
smart-contract-assistant/
├── backend/                    # Flask 后端服务
│   ├── app.py                 # 主应用程序
│   ├── requirements.txt       # Python 依赖包
│   ├── .env                  # 环境变量配置
│   └── knowledge_base/       # 本地知识库(可扩展)
├── frontend/                  # 前端界面
│   ├── index.html            # 门户主页
│   ├── assistant.html        # 智能助手交互页
│   ├── test.html             # API 测试页面
│   ├── assets/
│   │   ├── css/
│   │   │   └── style.css     # 所有样式文件
│   │   └── js/
│   │       └── app.js        # 所有前端逻辑
│   └── package.json          # 前端配置(可选)
└── README.md                 # 项目说明文档
```

## 🚀 快速开始

### 步骤 1：克隆与准备
```bash
# 克隆项目或按结构创建目录
mkdir smart-contract-assistant
cd smart-contract-assistant

# 创建目录结构
mkdir -p backend/knowledge_base frontend/assets/{css,js}
```

### 步骤 2：后端设置
```bash
# 进入后端目录
cd backend

# 安装 Python 依赖
pip install -r requirements.txt

# 创建并配置环境变量文件
cp .env.example .env  # 或直接创建 .env 文件
```

**编辑 `backend/.env` 文件：**
```env
# AI 服务 API 密钥 (必需)
AI_API_KEY=your_openai_or_compatible_api_key_here

# 应用访问密钥 (保护 /ask 接口)
APP_API_KEY=your_app_secret_key_here

# 服务器配置
PORT=5000
FLASK_DEBUG=true
```

### 步骤 3：前端配置
**编辑 `frontend/assets/js/app.js` 文件顶部：**
```javascript
const API_CONFIG = {
    BASE_URL: 'http://localhost:5000/api',
    API_KEY: 'your_app_secret_key_here'  // 与 backend/.env 中的 APP_API_KEY 保持一致
};
```

### 步骤 4：启动服务
```bash
# 终端 1：启动后端服务
cd backend
python app.py

# 终端 2：启动前端服务
cd frontend
python -m http.server 3000
```

### 步骤 5：访问应用
- 🌐 **门户主页**：[http://localhost:3000/index.html](http://localhost:3000/index.html)
- 🤖 **智能助手**：[http://localhost:3000/assistant.html](http://localhost:3000/assistant.html)
- 🧪 **API 测试**：[http://localhost:3000/test.html](http://localhost:3000/test.html)
- 🔧 **API 健康检查**：[http://localhost:5000/api/health](http://localhost:5000/api/health)

## ⚙️ 详细配置

### 后端配置 (`backend/app.py` 顶部)
```python
# ========== 配置区域 ==========
AI_PROVIDER = 'openai_compatible'  # 或 'mock' 使用模拟模式
AI_MODEL = 'qwen3-next-80b-a3b-thinking'  # 使用的 AI 模型
OPENAI_COMPATIBLE_BASE_URL = 'https://dashscope.aliyuncs.com/compatible-mode/v1'  # 兼容接口地址
# ========== 配置区域结束 ==========
```

### 支持的服务商
1. **阿里云百炼**：使用上述默认配置
2. **OpenAI 官方**：
   ```python
   OPENAI_COMPATIBLE_BASE_URL = 'https://api.openai.com/v1'
   ```
3. **其他兼容服务**：修改为对应的 API 端点

### 模拟模式
如需快速测试或避免 API 调用，可启用模拟模式：
```python
AI_PROVIDER = 'mock'  # 使用本地知识库回答问题
```

## 📡 API 文档

### 基础信息
- **Base URL**: `http://localhost:5000/api`
- **认证方式**: 所有请求需在 Header 中添加 `X-API-Key: your_app_secret_key_here`

### 可用端点

#### 1. 健康检查
```http
GET /api/health
```
**响应示例：**
```json
{
  "status": "healthy",
  "service": "smart_contract_assistant",
  "timestamp": "2023-10-01T12:00:00.000Z",
  "provider": "openai_compatible",
  "model": "qwen3-next-80b-a3b-thinking"
}
```

#### 2. 服务信息
```http
GET /api/info
```
**响应示例：**
```json
{
  "service_name": "智能合约问答助手",
  "version": "2.0",
  "provider": "openai_compatible",
  "model": "qwen3-next-80b-a3b-thinking",
  "status": "active",
  "requires_api_key": true
}
```

#### 3. 智能问答 (核心功能)
```http
POST /api/ask
Headers: {
  "Content-Type": "application/json",
  "X-API-Key": "your_app_secret_key_here"
}
Body: {
  "question": "如何编写一个安全的ERC20合约？"
}
```
**响应示例：**
```json
{
  "success": true,
  "question": "如何编写一个安全的ERC20合约？",
  "answer": "编写安全的ERC20合约需要注意以下要点：\n1. 使用OpenZeppelin合约库...",
  "model": "qwen3-next-80b-a3b-thinking",
  "tokens_used": 256,
  "source": "ai_service"
}
```

## 🛠 故障排除

### 常见问题

#### 1. **后端启动失败：`ModuleNotFoundError`**
```bash
# 确保安装所有依赖
cd backend
pip install -r requirements.txt

# 如果缺少个别包
pip install flask flask-cors python-dotenv openai httpx
```

#### 2. **前端连接失败：网络错误**
```javascript
// 检查 frontend/assets/js/app.js 中的配置
const API_CONFIG = {
    BASE_URL: 'http://localhost:5000/api',  // 端口必须与后端一致
    API_KEY: 'your_app_secret_key_here'     // 必须与 backend/.env 的 APP_API_KEY 一致
};
```

#### 3. **API 密钥错误**
- 确保 `backend/.env` 中的 `APP_API_KEY` 与 `frontend/assets/js/app.js` 中的 `API_KEY` 完全一致
- 重启前后端服务使配置生效

#### 4. **OpenAI 版本兼容性问题**
如果遇到 `proxies` 参数错误，已在内置代码中自动处理。如需手动修复：
```bash
# 确保安装正确版本
pip install openai==1.3.0 httpx==0.24.1
```

### 端口冲突处理
如果端口 5000 或 3000 已被占用：

1. **修改后端端口**：
   ```bash
   # 修改 backend/.env 中的 PORT
   PORT=5001
   ```

2. **更新前端配置**：
   ```javascript
   // 修改 frontend/assets/js/app.js
   BASE_URL: 'http://localhost:5001/api'
   ```

## 🔍 开发与扩展

### 添加知识库条目
编辑 `backend/app.py` 中的 `get_mock_response` 函数，扩展 `qa_pairs` 字典：
```python
qa_pairs = {
    "智能合约": "...",
    "ERC20": "...",
    # 添加新的关键词和答案
    "NFT": "NFT（非同质化代币）是独特的数字资产...",
    "DeFi": "DeFi（去中心化金融）是基于区块链的金融服务..."
}
```

### 自定义前端样式
所有样式集中在 `frontend/assets/css/style.css`，修改 CSS 变量即可调整主题：
```css
:root {
    --primary-cyan: #00f2fe;      /* 主色调 - 青色 */
    --primary-purple: #4facfe;    /* 主色调 - 紫色 */
    --dark-bg: #0a0a0f;          /* 背景色 */
    --card-bg: rgba(20, 25, 40, 0.7); /* 卡片背景 */
    /* 修改这些值来自定义配色 */
}
```

### 添加新 API 端点
在 `backend/app.py` 中添加新的路由：
```python
@app.route('/api/new-endpoint', methods=['GET'])
@require_app_key  # 如果需要认证
def new_endpoint():
    return jsonify({"message": "新端点工作正常"})
```

## 📄 许可证与声明

### 使用条款
1. 本项目仅供学习与开发参考
2. 生成的智能合约代码应在生产环境前进行完整安全审计
3. AI 回答可能存在不准确之处，请结合官方文档验证

### 免责声明
本项目开发者不对以下情况负责：
- 使用本项目产生的直接或间接损失
- 基于 AI 生成代码部署到主网导致的资产损失
- 因 API 密钥泄露导致的安全问题

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来改进项目：
1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📞 支持与联系

遇到问题？请按以下步骤：
1. 查看本 README 的故障排除部分
2. 检查 Issues 中是否有类似问题
3. 提交新的 Issue，包含：
   - 错误信息
   - 复现步骤
   - 环境信息 (Python 版本、操作系统等)

---

**Happy Building!** 🚀 祝你在 Web3 开发之旅中一帆风顺！

*如果这个项目对你有帮助，请给个 Star ⭐ 支持！*
