import streamlit as st
import streamlit.components.v1 as components

# 设置页面配置（宽屏模式，更像真正的 App）
st.set_page_config(page_title="Hometree - Find Your Soul", layout="wide", initial_sidebar_state="collapsed")

# ==========================================
# 核心：注入顶级 CSS 和 前端交互逻辑
# ==========================================
html_code = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root {
            --bg-color: #FFF0F5;
            --text-color: #333;
            --card-bg: #FFFFFF;
            --accent: #FF69B4;
            --accent-light: #FFB6C1;
            --border: #FFE4E1;
        }
        [data-theme="dark"] {
            --bg-color: #1A1A1A;
            --text-color: #F5F5F5;
            --card-bg: #2C2C2C;
            --accent: #FF1493;
            --accent-light: #8B008B;
            --border: #444;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        body { background-color: var(--bg-color); color: var(--text-color); transition: all 0.3s; overflow-x: hidden; }
        
        /* 顶部导航 */
        .navbar { display: flex; justify-content: space-between; align-items: center; padding: 20px; background: var(--card-bg); box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
        .logo { font-size: 24px; font-weight: 800; color: var(--accent); display: flex; align-items: center; gap: 8px; }
        .theme-toggle { cursor: pointer; font-size: 20px; background: none; border: none; color: var(--text-color); }

        /* 主布局：左边匹配，右边聊天 */
        .main-container { display: flex; height: calc(100vh - 80px); max-width: 1200px; margin: 0 auto; padding: 20px; gap: 20px; }
        
        /* 左侧：Tinder 风格卡片 */
        .card-section { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        .match-card { width: 100%; max-width: 380px; background: var(--card-bg); border-radius: 24px; overflow: hidden; box-shadow: 0 20px 40px rgba(255, 105, 180, 0.15); position: relative; transition: transform 0.3s; }
        .match-card:hover { transform: translateY(-5px); }
        .cover-img { width: 100%; height: 400px; object-fit: cover; border-bottom: 4px solid var(--accent); }
        .card-info { padding: 20px; }
        .card-name { font-size: 22px; font-weight: bold; margin-bottom: 5px; }
        .card-tags { font-size: 14px; color: var(--accent); margin-bottom: 15px; }
        .ai-agent-box { background: var(--bg-color); border-left: 4px solid var(--accent); padding: 10px; font-size: 13px; font-style: italic; border-radius: 4px; margin-bottom: 15px; }
        .btn-group { display: flex; justify-content: space-around; padding: 0 20px 20px; }
        .action-btn { width: 60px; height: 60px; border-radius: 50%; border: none; font-size: 24px; cursor: pointer; box-shadow: 0 5px 15px rgba(0,0,0,0.1); transition: 0.2s; display: flex; justify-content: center; align-items: center;}
        .btn-dislike { background: #fff; color: #ccc; }
        .btn-like { background: var(--accent); color: white; }
        .action-btn:hover { transform: scale(1.1); }

        /* 右侧：聊天界面 */
        .chat-section { flex: 1; background: var(--card-bg); border-radius: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); display: flex; flex-direction: column; overflow: hidden; }
        .chat-header { padding: 15px 20px; border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 10px; font-weight: bold; }
        .chat-messages { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; }
        .msg { max-width: 80%; padding: 10px 15px; border-radius: 18px; font-size: 14px; line-height: 1.4; }
        .msg-left { background: var(--border); align-self: flex-start; border-bottom-left-radius: 4px; }
        .msg-right { background: var(--accent); color: white; align-self: flex-end; border-bottom-right-radius: 4px; }
        .chat-input-area { padding: 15px; border-top: 1px solid var(--border); display: flex; gap: 10px; }
        .chat-input-area input { flex: 1; padding: 12px 20px; border-radius: 30px; border: 1px solid var(--border); background: var(--bg-color); color: var(--text-color); outline: none; }
        .chat-input-area button { padding: 0 20px; border-radius: 30px; border: none; background: var(--accent); color: white; cursor: pointer; font-weight: bold; }

        /* 悬浮 AI 助手 */
        .ai-assistant { position: fixed; bottom: 30px; right: 30px; width: 60px; height: 60px; background: var(--accent); border-radius: 50%; display: flex; justify-content: center; align-items: center; color: white; font-size: 30px; cursor: pointer; box-shadow: 0 10px 20px rgba(255,105,180,0.4); animation: float 3s ease-in-out infinite; }
        @keyframes float { 0% { transform: translateY(0); } 50% { transform: translateY(-10px); } 100% { transform: translateY(0); } }
    </style>
</head>
<body data-theme="light">

    <div class="navbar">
        <div class="logo">🌸 Hometree</div>
        <button class="theme-toggle" onclick="toggleTheme()">🌙</button>
    </div>

    <div class="main-container">
        <!-- 左侧匹配卡片 -->
        <div class="card-section">
            <div class="match-card">
                <img src="https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?auto=format&fit=crop&w=800&q=80" class="cover-img" alt="Profile">
                <div class="card-info">
                    <div class="card-name">Yuki, 21</div>
                    <div class="card-tags">🎵 The Smiths, 落日飞车 · 📚 三岛由纪夫</div>
                    
                    <!-- AI Agent 提取分析 -->
                    <div class="ai-agent-box">
                        🤖 <b>AI Agent Insight:</b> "You both love The Smiths and indie films. A great conversation starter: Ask about her favorite track on 'The Queen Is Dead'."
                    </div>

                    <div class="btn-group">
                        <button class="action-btn btn-dislike" onclick="alert('Passed. Algorithm adjusting...')">✕</button>
                        <button class="action-btn btn-like" onclick="matched()">♥</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- 右侧聊天 (Tinder式匹配后解锁) -->
        <div class="chat-section" id="chatUI" style="opacity: 0.3; pointer-events: none;">
            <div class="chat-header">
                <img src="https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?auto=format&fit=crop&w=80&q=80" style="width:40px;height:40px;border-radius:50%;object-fit:cover;">
                Chat with Yuki
            </div>
            <div class="chat-messages" id="chatBox">
                <div class="msg msg-left">Hey! I saw you also listen to Cigarettes After Sex. Their new album is amazing.</div>
                <div class="msg msg-right" id="aiGeneratedMsg" style="display:none;">That's so cool! We should link our NetEase Cloud Music playlists.</div>
            </div>
            <div class="chat-input-area">
                <input type="text" placeholder="Say something nice...">
                <button>Send</button>
            </div>
        </div>
    </div>

    <!-- 悬浮 AI 助手 -->
    <div class="ai-assistant" onclick="generateAIMessage()">🤖</div>

    <script>
        // 白天/黑夜模式切换
        function toggleTheme() {
            const body = document.body;
            const btn = document.querySelector('.theme-toggle');
            if (body.getAttribute('data-theme') === 'light') {
                body.setAttribute('data-theme', 'dark');
                btn.innerText = '☀️';
            } else {
                body.setAttribute('data-theme', 'light');
                btn.innerText = '🌙';
            }
        }

        // 模拟匹配成功
        function matched() {
            const chatUI = document.getElementById('chatUI');
            chatUI.style.opacity = '1';
            chatUI.style.pointerEvents = 'auto';
            alert("🎉 It's a Match! You can now chat with Yuki.");
        }

        // 模拟 AI Agent 自动生成破冰语
        function generateAIMessage() {
            const msgBox = document.getElementById('chatBox');
            const newMsg = document.createElement('div');
            newMsg.className = 'msg msg-right';
            newMsg.innerText = "Hey Yuki, my AI Assistant suggests we both have immaculate taste in 80s indie rock. What's your favorite vinyl?";
            msgBox.appendChild(newMsg);
            msgBox.scrollTop = msgBox.scrollHeight;
        }
    </script>
</body>
</html>
"""

# 将这段高级前端代码嵌入到 Streamlit 页面中
components.html(html_code, height=900, scrolling=True)
