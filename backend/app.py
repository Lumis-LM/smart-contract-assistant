import os
import datetime
import random
import time
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
from dotenv import load_dotenv


# ========== 配置区域：在此修改AI服务、模型等 ==========
# AI服务提供商: 'openai_compatible' 或 'mock'
AI_PROVIDER = 'openai_compatible'  # 先用模拟模式
# 模型名称 (根据所选提供商填写)
AI_MODEL = 'qwen3-next-80b-a3b-thinking'
# OpenAI兼容接口的基址 (阿里云百炼、OpenAI官方等)
OPENAI_COMPATIBLE_BASE_URL = 'https://dashscope.aliyuncs.com/compatible-mode/v1'

# ========== 配置区域结束 ==========

# 加载环境变量
load_dotenv()
app = Flask(__name__)
CORS(app)

# 初始化AI客户端（适用于OpenAI >= 1.0.0）
ai_client = None
if AI_PROVIDER == 'openai_compatible':
    try:
        import openai

        api_key = os.getenv("AI_API_KEY")

        if not api_key:
            print("⚠️  未找到AI_API_KEY，将使用模拟模式")
            AI_PROVIDER = 'mock'
        else:
            print(f"📦 OpenAI库版本: {openai.__version__}")

            # 关键修改：创建自定义的httpx客户端以处理代理或配置问题
            import httpx

            # 方案A：如果你的网络环境不需要代理，使用基础配置
            try:
                # 创建一个基础httpx客户端，设置超时
                http_client = httpx.Client(timeout=30.0)
                ai_client = openai.OpenAI(
                    api_key=api_key,
                    base_url=OPENAI_COMPATIBLE_BASE_URL,
                    http_client=http_client  # 显式传入自定义客户端
                )
                print("✅ AI服务客户端已初始化 (使用基础HTTP客户端)")

            except TypeError as e:
                # 方案B：如果方案A因环境问题失败，尝试更彻底的配置
                print(f"⚠️  基础初始化遇到问题 ({e})，尝试清理环境变量后重试...")
                # 清除可能干扰的环境变量
                for key in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY']:
                    os.environ.pop(key, None)

                # 重新创建简单的httpx客户端
                http_client = httpx.Client(timeout=30.0)
                ai_client = openai.OpenAI(
                    api_key=api_key,
                    base_url=OPENAI_COMPATIBLE_BASE_URL,
                    http_client=http_client
                )
                print("✅ AI服务客户端已初始化 (清理环境变量后)")

            print(f"✅ 模型: {AI_MODEL}")

    except ImportError:
        print("⚠️  未安装openai库，将使用模拟模式。请执行: pip install openai httpx")
        AI_PROVIDER = 'mock'
    except Exception as e:
        print(f"❌ OpenAI客户端初始化失败: {e}")
        print("⚠️  将使用模拟模式")
        AI_PROVIDER = 'mock'
elif AI_PROVIDER == 'mock':
    print("ℹ️  运行在模拟模式")
else:
    print(f"⚠️  未知的AI_PROVIDER配置: {AI_PROVIDER}，将使用模拟模式")
    AI_PROVIDER = 'mock'

# 应用自身API密钥 (用于保护/ask接口)
APP_API_KEY = os.getenv("APP_API_KEY", "your-secret-key-here")
def require_app_key(f):
    """验证应用API密钥的装饰器"""

    @wraps(f)
    def decorated(*args, **kwargs):
        client_key = request.headers.get('X-API-Key')

        # 调试信息
        print(f"📨 收到请求 - 路径: {request.path}")
        print(f"🔑 客户端发送的密钥: '{client_key}'")

        if not client_key:
            print("❌ 请求头中缺少 X-API-Key")
            return jsonify({"error": "缺少API密钥"}), 401

        if client_key != APP_API_KEY:
            print(f"❌ API密钥不匹配！期望: '{APP_API_KEY}'")
            return jsonify({"error": "无效的API密钥"}), 401

        print("✅ API密钥验证通过")
        return f(*args, **kwargs)

    return decorated


def get_ai_response(question):
    """调用AI服务获取响应 (核心函数)"""
    if AI_PROVIDER == 'openai_compatible' and ai_client:
        return get_openai_compatible_response(question)
    else:
        return get_mock_response(question)


def get_openai_compatible_response(question):
    """通过OpenAI兼容接口调用AI服务 (适用于OpenAI >= 1.0.0)"""
    messages = [
        {"role": "system", "content": "你是一位智能合约专家，回答需准确、易懂，并提供代码示例和安全建议。"},
        {"role": "user", "content": question}
    ]
    try:
        # 使用新版本的调用方式
        response = ai_client.chat.completions.create(
            model=AI_MODEL,
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        return {
            "answer": response.choices[0].message.content,
            "model": response.model,
            "tokens_used": response.usage.total_tokens,
            "source": "ai_service"
        }
    except Exception as e:
        error_msg = f"AI服务调用失败: {str(e)}"
        print(f"❌ {error_msg}")
        # 即使这里降级到模拟模式，也已不再是因版本问题
        return get_mock_response(question, api_error=True, error_detail=error_msg)


def get_mock_response(question, api_error=False, error_detail=""):
    """模拟响应 (降级方案)"""
    time.sleep(0.5)

    # 知识库
    qa_pairs = {
        "智能合约": "智能合约是部署在区块链上的自执行代码，当预定条件满足时自动执行，无需中介。特点：去中心化、透明、不可篡改。",
        "ERC20": "ERC20是以太坊上同质化代币的标准接口，包含transfer、balanceOf等基本函数。",
        "安全风险": "常见风险包括：重入攻击、整数溢出、访问控制缺陷。防范措施：使用检查-效果-交互模式、进行代码审计。",
        "Solidity": "Solidity是用于编写以太坊智能合约的主流面向对象语言，语法类似JavaScript。"
    }

    # 匹配问题
    answer_content = None
    q_lower = question.lower()
    for key in qa_pairs:
        if key.lower() in q_lower:
            answer_content = qa_pairs[key]
            break

    if not answer_content:
        answer_content = random.choice([
            "智能合约通过代码定义和执行合约条款，实现去信任化的自动化交易。",
            "编写安全合约需注意：最小权限原则、输入验证、使用审计过的库。"
        ])

    # 构建响应
    if api_error:
        prefix = f"⚠️ AI服务暂时不可用 ({error_detail[:50]}...)\n\n模拟答案：\n"
    else:
        prefix = "💡 模拟模式答案：\n"

    return {
        "answer": f"{prefix}{answer_content}\n\n（如需实时AI回答，请配置有效的AI_API_KEY）",
        "model": "local_knowledge_base",
        "tokens_used": 0,
        "source": "mock"
    }


@app.route('/api/health')
def health_check():
    """健康检查接口"""
    return jsonify({
        "status": "healthy",
        "service": "smart_contract_assistant",
        "timestamp": datetime.datetime.now().isoformat(),
        "provider": AI_PROVIDER,
        "model": AI_MODEL if AI_PROVIDER != 'mock' else None
    })


@app.route('/api/info')
def service_info():
    """服务信息接口"""
    return jsonify({
        "service_name": "智能合约问答助手",
        "version": "2.0",
        "provider": AI_PROVIDER,
        "model": AI_MODEL if AI_PROVIDER != 'mock' else "local_knowledge_base",
        "status": "active" if AI_PROVIDER != 'mock' else "mock_mode",
        "requires_api_key": True
    })


@app.route('/api/ask', methods=['POST'])
@require_app_key
def ask():
    """主问答API接口"""
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({"error": "缺少问题参数"}), 400

        question = data['question'].strip()
        if not question:
            return jsonify({"error": "问题内容为空"}), 400

        result = get_ai_response(question)
        return jsonify({
            "success": True,
            "question": question,
            "answer": result["answer"],
            "model": result["model"],
            "tokens_used": result["tokens_used"],
            "source": result["source"]
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"服务器内部错误: {str(e)[:100]}"
        }), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    print("\n" + "=" * 55)
    print("🚀 智能合约问答助手 API 启动成功")
    print("=" * 55)
    print(f"📍 API地址: http://127.0.0.1:{port}/api")
    print(f"🔧 调试模式: {debug}")
    print(f"🤖 服务模式: {AI_PROVIDER.upper().replace('_', ' ')}")
    if AI_PROVIDER != 'mock':
        print(f"📦 AI 模型: {AI_MODEL}")
    print(f"🔑 应用密钥: {APP_API_KEY}")
    print("\n📎 API端点:")
    print(f"   📊 健康检查: GET http://127.0.0.1:{port}/api/health")
    print(f"   ℹ️  服务信息: GET http://127.0.0.1:{port}/api/info")
    print(f"   ❓ 问答接口: POST http://127.0.0.1:{port}/api/ask")

    if AI_PROVIDER == 'mock':
        print("\n💡 当前为模拟模式，如需使用真实AI服务：")
        print("   1. 获取AI API密钥（如阿里云百炼、OpenAI等）")
        print("   2. 在backend/.env中设置 AI_API_KEY=你的密钥")
        print("   3. 在app.py中设置 AI_PROVIDER = 'openai_compatible'")
        print("   4. 重启应用")

    print("=" * 55)
    app.run(host='0.0.0.0', port=port, debug=debug)

