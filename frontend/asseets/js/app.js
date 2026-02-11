// 配置 - 后端API地址和密钥 (与backend/.env中的APP_API_KEY保持一致)
const API_CONFIG = {
    BASE_URL: 'http://localhost:5000/api',
    API_KEY: 'your_app_secret_key_here' // 请确保与后端APP_API_KEY一致
};

// ===== 通用工具函数 =====
async function makeApiRequest(endpoint, method = 'GET', data = null) {
    const headers = {
        'Content-Type': 'application/json',
        'X-API-Key': API_CONFIG.API_KEY
    };
    const options = {
        method,
        headers,
    };
    if (data && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(data);
    }
    try {
        console.log(`🌐 请求: ${method} ${API_CONFIG.BASE_URL}${endpoint}`);
        const response = await fetch(`${API_CONFIG.BASE_URL}${endpoint}`, options);
        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.error || `HTTP ${response.status}`);
        }
        return result;
    } catch (error) {
        console.error('❌ API请求失败:', error);
        throw error;
    }
}

// ===== 主页功能 =====
function initHomePage() {
    // 文档按钮点击事件
    const docsBtn = document.getElementById('viewDocs');
    if (docsBtn) {
        docsBtn.addEventListener('click', () => {
            alert('文档功能开发中，敬请期待！');
        });
    }
    // 特性卡片动画
    const cards = document.querySelectorAll('.feature-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
}

// ===== 助手页面功能 =====
function initAssistantPage() {
    // 页面元素
    const questionInput = document.getElementById('questionInput');
    const sendButton = document.getElementById('sendButton');
    const messagesContainer = document.getElementById('messagesContainer');
    const exampleChips = document.querySelectorAll('.question-chip');
    let messageCount = 1;

    // 自动调整输入框高度
    questionInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });

    // 示例问题点击
    exampleChips.forEach(chip => {
        chip.addEventListener('click', function() {
            questionInput.value = this.textContent;
            questionInput.focus();
            questionInput.dispatchEvent(new Event('input'));
        });
    });

    // 发送问题
    async function sendQuestion() {
        const question = questionInput.value.trim();
        if (!question) return;

        // 禁用按钮，添加用户消息
        sendButton.disabled = true;
        addMessage(question, 'user');
        questionInput.value = '';
        questionInput.style.height = '60px';

        // 添加AI思考中的占位消息
        const thinkingMsgId = addThinkingMessage();

        try {
            const response = await makeApiRequest('/ask', 'POST', { question });
            // 移除“思考中”消息
            removeMessage(thinkingMsgId);
            // 添加AI回复
            addMessage(response.answer, 'ai', response.model, response.tokens_used, response.source);
            updateStats(response.model, response.tokens_used, response.source);
        } catch (error) {
            removeMessage(thinkingMsgId);
            addMessage(`**请求出错**: ${error.message || '未知错误'}`, 'ai', 'Error', 0, 'error');
        } finally {
            sendButton.disabled = false;
        }
    }

    // 添加消息到界面
    function addMessage(content, sender, model = null, tokens = 0, source = null) {
        messageCount++;
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const now = new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
        let headerHtml = `<span><i class="fas fa-${sender === 'user' ? 'user' : 'robot'}"></i> ${sender === 'user' ? 'You' : 'Contract Assistant'}</span>`;
        headerHtml += `<span>${now}</span>`;

        // 格式化消息内容
        let formattedContent = content
            .replace(/\n/g, '<br>')
            .replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
            .replace(/`([^`]+)`/g, '<code>$1</code>');

        let extraInfo = '';
        if (sender === 'ai' && model) {
            const sourceText = source === 'mock' ? '本地知识库' : 'AI 服务';
            extraInfo = `<div class="message-meta">
                <i class="fas fa-microchip"></i> 模型: ${model} | 
                <i class="fas fa-hashtag"></i> Token: ${tokens} | 
                <i class="fas fa-database"></i> 来源: ${sourceText}
            </div>`;
        }

        messageDiv.innerHTML = `
            <div class="message-header">${headerHtml}</div>
            <div class="message-content">${formattedContent}${extraInfo}</div>
        `;
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        document.getElementById('messageCount').textContent = messageCount;
        return messageDiv;
    }

    // 添加"思考中"消息
    function addThinkingMessage() {
        messageCount++;
        const thinkingDiv = document.createElement('div');
        thinkingDiv.className = 'message ai-message';
        thinkingDiv.id = 'thinkingMsg';
        thinkingDiv.innerHTML = `
            <div class="message-header">
                <span><i class="fas fa-robot"></i> Contract Assistant</span>
                <span>现在</span>
            </div>
            <div class="message-content">
                <p><i class="fas fa-cog fa-spin"></i> 正在思考，请稍候...</p>
            </div>
        `;
        messagesContainer.appendChild(thinkingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        return 'thinkingMsg';
    }

    // 移除消息
    function removeMessage(id) {
        const element = document.getElementById(id);
        if (element) {
            element.remove();
            messageCount--;
            document.getElementById('messageCount').textContent = messageCount;
        }
    }

    // 更新状态栏
    function updateStats(model, tokens, source) {
        document.getElementById('currentModel').textContent = model || 'qwen3-next-80b';
        document.getElementById('tokenUsed').textContent = tokens || 0;
        document.getElementById('responseSource').textContent = source === 'mock' ? '本地知识库' : 'AI 服务';
    }

    // 事件监听
    sendButton.addEventListener('click', sendQuestion);
    questionInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendQuestion();
        }
    });

    // 初始化
    questionInput.focus();
}

// ===== 页面初始化 =====
document.addEventListener('DOMContentLoaded', function() {
    // 根据当前页面初始化不同功能
    if (document.querySelector('.hero')) {
        initHomePage(); // 首页
    }
    if (document.getElementById('messagesContainer')) {
        initAssistantPage(); // 助手页
    }

    // 全局：测试后端连接
    testBackendConnection();
});

// 测试后端连接
async function testBackendConnection() {
    try {
        const health = await makeApiRequest('/health');
        console.log('✅ 后端连接正常:', health);
        // 更新状态指示器（如果存在）
        const statusDot = document.querySelector('.status-dot');
        if (statusDot && health.status === 'healthy') {
            statusDot.style.backgroundColor = 'var(--success)';
        }
    } catch (error) {
        console.warn('⚠️ 后端连接测试失败，请确保后端服务正在运行');
    }
}
