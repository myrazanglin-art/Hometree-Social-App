import streamlit as st
import streamlit.components.v1 as components

# 使用 wide 模式，并且隐藏 Streamlit 默认的顶部 padding，让嵌入的页面完全铺满
st.set_page_config(page_title="Hometree", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
        /* 隐藏 Streamlit 默认的元素，防止干扰 iframe 的点击 */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container { padding-top: 0rem; padding-bottom: 0rem; max-width: 100%; }
        iframe { width: 100%; height: 100vh; border: none; }
    </style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        /* 日间与夜间模式的 CSS 变量 */
        :root {
            --bg: #F5F5F7;
            --panel: #FFFFFF;
            --text: #1D1D1F;
            --sub: #86868B;
            --border: #E5E5EA;
            --accent: #FF69B4;
            --card-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        [data-theme="dark"] {
            --bg: #121212;
            --panel: #1E1E1E;
            --text: #F2F2F7;
            --sub: #8E8E93;
            --border: #333333;
            --accent: #FF1493;
            --card-shadow: 0 10px 30px rgba(0,0,0,0.8);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background: var(--bg); color: var(--text); height: 100vh; overflow: hidden; transition: background 0.3s, color 0.3s; }

        /* 布局框架 */
        .layout { display: flex; height: 100vh; width: 100vw; }
        
        /* 左侧信息栏 */
        .sidebar { width: 250px; border-right: 1px solid var(--border); padding: 20px; background: var(--panel); flex-shrink: 0; }
        .logo { font-size: 24px; font-weight: 900; color: var(--accent); letter-spacing: -1px; margin-bottom: 30px;}
        .user-panel { display: flex; align-items: center; gap: 10px; margin-bottom: 30px; }
        .user-panel img { width: 50px; height: 50px; border-radius: 12px; border: 2px solid var(--accent); object-fit: cover;}
        .nav-item { padding: 12px 0; color: var(--sub); font-size: 14px; cursor: pointer; border-bottom: 1px dashed var(--border); display: flex; justify-content: space-between;}
        .nav-item:hover { color: var(--accent); }

        /* 中间滑动区 */
        .main-feed { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; background: var(--bg); }
        
        /* 卡片容器 */
        .card-container { width: 380px; height: 550px; position: relative; }
        
        /* 卡片样式 */
        .card { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: var(--panel); border-radius: 24px; border: 1px solid var(--border); box-shadow: var(--card-shadow); overflow: hidden; display: flex; flex-direction: column; transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), opacity 0.4s ease; }
        
        .card-img { width: 100%; height: 60%; object-fit: cover; }
        .card-content { padding: 20px; flex: 1; display: flex; flex-direction: column; }
        
        .name-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
        .name { font-size: 24px; font-weight: bold; }
        .tags { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 15px; }
        .tag { background: var(--bg); border: 1px solid var(--border); color: var(--accent); padding: 4px 10px; border-radius: 8px; font-size: 12px; }
        .quote { font-size: 14px; color: var(--sub); font-style: italic; border-left: 2px solid var(--accent); padding-left: 10px; margin-bottom: 15px; }
        .ai-agent { font-size: 12px; color: var(--accent); font-family: monospace; margin-top: auto; background: var(--bg); padding: 10px; border-radius: 8px; }

        /* 操作按钮 */
        .controls { margin-top: 30px; display: flex; gap: 20px; }
        .btn { width: 65px; height: 65px; border-radius: 50%; border: 2px solid var(--border); background: var(--panel); color: var(--text); font-size: 24px; cursor: pointer; display: flex; justify-content: center; align-items: center; box-shadow: var(--card-shadow); transition: 0.2s; }
        .btn:hover { transform: scale(1.1); border-color: var(--accent); color: var(--accent); }
        .btn-like { width: 75px; height: 75px; font-size: 30px; border-color: var(--accent); color: var(--accent); }
        
        /* 右侧动态栏 */
        .right-panel { width: 280px; border-left: 1px solid var(--border); padding: 20px; background: var(--panel); overflow-y: auto; flex-shrink: 0; }
        .feed-title { font-size: 14px; font-weight: bold; margin-bottom: 15px; border-bottom: 1px solid var(--border); padding-bottom: 10px; }
        .feed-item { font-size: 13px; color: var(--sub); margin-bottom: 15px; line-height: 1.4; padding-left: 10px; border-left: 2px solid var(--border); }
        .feed-item span { color: var(--accent); font-weight: bold; }

        /* 顶部导航 */
        .top-nav { position: absolute; top: 20px; right: 20px; display: flex; gap: 10px; z-index: 100; }
        .theme-btn { width: 40px; height: 40px; border-radius: 50%; border: 1px solid var(--border); background: var(--panel); color: var(--text); cursor: pointer; display: flex; justify-content: center; align-items: center; font-size: 18px; box-shadow: var(--card-shadow); }
        
        /* 匹配弹窗 */
        .modal { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: var(--panel); z-index: 1000; display: none; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 40px; }
        .modal h1 { color: var(--accent); font-size: 32px; margin-bottom: 20px; }
        .modal button { padding: 15px 30px; border-radius: 30px; background: var(--accent); color: #FFF; border: none; font-size: 16px; cursor: pointer; margin-top: 30px; }
    </style>
</head>
<body data-theme="light">

    <!-- 顶部模式切换 -->
    <div class="top-nav">
        <button class="theme-btn" onclick="toggleTheme()">🌙</button>
    </div>

    <div class="layout">
        
        <!-- 左侧栏 -->
        <div class="sidebar">
            <div class="logo">Hometree.</div>
            <div class="user-panel">
                <img src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=100&q=80">
                <div>
                    <h3 style="font-size:16px;">Yiming</h3>
                    <p style="font-size:12px;color:var(--sub);">Find your frequency</p>
                </div>
            </div>
            <div class="nav-item"><span>📂 我的书影音</span></div>
            <div class="nav-item"><span>💬 消息 (1)</span></div>
            <div class="nav-item"><span>⚙ 设置</span></div>
        </div>

        <!-- 中间卡片区 -->
        <div class="main-feed">
            <div class="card-container" id="cardContainer">
                <!-- 卡片生成处 -->
            </div>
            
            <div class="controls">
                <button class="btn" onclick="swipe('left')">✕</button>
                <button class="btn btn-like" onclick="swipe('right')">♥</button>
            </div>
        </div>

        <!-- 右侧动态栏 -->
        <div class="right-panel">
            <div class="feed-title">Live Activity</div>
            <div class="feed-item"><span>娄烨</span> 正在看《苏州河》</div>
            <div class="feed-item"><span>Tyler Durden</span> 创建了新的搏击俱乐部</div>
            <div class="feed-item"><span>Björk</span> 分享了新的实验电子歌单</div>
            <div class="feed-item"><span>罗大佑</span> 演唱了《鹿港小镇》</div>
            <div class="feed-item"><span>The Smiths</span> 刚刚上线</div>
        </div>

    </div>

    <!-- 匹配弹窗 -->
    <div class="modal" id="matchModal">
        <h1>FREQUENCY ALIGNED.</h1>
        <p>你们的精神频率已对齐。</p>
        <button onclick="closeMatch()">发送消息</button>
    </div>

    <script>
        // 10 个亚文化用户数据
        const users = [
            { name: "娄烨", img: "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=500", tags: ["苏州河", "摇晃镜头"], quote: "如果有一天我走了，你会像马达那样找我吗？", ai: "AI: 适合在雨天聊贾宏声。" },
            { name: "Tyler Durden", img: "https://images.unsplash.com/photo-1520637836862-4d197d17c90a?w=500", tags: ["Fight Club", "Nihilism"], quote: "You are not your job.", ai: "AI: 别聊工作，聊地下搏击。" },
            { name: "The Smiths", img: "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?w=500", tags: ["Jangle Pop", "Morrissey"], quote: "There is a light that never goes out.", ai: "AI: 深夜 emo 必备。" },
            { name: "Björk", img: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=500", tags: ["Art Pop", "Homogenic"], quote: "I'm the spark.", ai: "AI: 冰岛极光与实验电子。" },
            { name: "Muse", img: "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=500", tags: ["Space Rock", "Falsetto"], quote: "This is the last time I'll abandon you.", ai: "AI: 科幻与反乌托邦同好。" },
            { name: "罗大佑", img: "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=500", tags: ["鹿港小镇", "时代挽歌"], quote: "台北不是我的家。", ai: "AI: 午夜聊华语启蒙。" },
            { name: "Midwest Emo", img: "https://images.unsplash.com/photo-1501386761578-eac5c94b800a?w=500", tags: ["Math Rock", "Delay"], quote: "Let's just play in drop D.", ai: "AI: 沉浸效果器的男孩。" },
            { name: "Aphex Twin", img: "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=500", tags: ["IDM", "Ambient"], quote: "Weird music for weird people.", ai: "AI: Max/MSP 同好。" },
            { name: "Kurt Cobain", img: "https://images.unsplash.com/photo-1520637836862-4d197d17c90a?w=500", tags: ["Grunge", "Nirvana"], quote: "I'd rather be hated for who I am.", ai: "AI: 聊聊地下厂牌。" },
            { name: "Kevin Shields", img: "https://images.unsplash.com/photo-1516280440502-863a346513c1?w=500", tags: ["Shoegaze", "MBV"], quote: "Loveless is a wall of sound.", ai: "AI: 噪音墙之神。" }
        ];

        let currentIndex = 0;
        const container = document.getElementById('cardContainer');

        // 初始化渲染卡片
        function renderCards() {
            container.innerHTML = '';
            // 从后往前渲染，让第一个在最上面
            for (let i = users.length - 1; i >= 0; i--) {
                const user = users[i];
                const card = document.createElement('div');
                card.className = 'card';
                // 计算堆叠偏移
                const offset = i - currentIndex;
                
                if (offset < 0) {
                    card.style.display = 'none'; // 已经滑过的
                } else {
                    card.style.transform = `scale(${1 - offset * 0.05}) translateY(${offset * 10}px)`;
                    card.style.zIndex = -offset;
                    card.style.opacity = 1 - offset * 0.2;
                    
                    card.innerHTML = `
                        <img src="${user.img}" class="card-img">
                        <div class="card-content">
                            <div class="name-row"><div class="name">${user.name}</div></div>
                            <div class="tags">${user.tags.map(t => `<span class="tag">${t}</span>`).join('')}</div>
                            <div class="quote">"${user.quote}"</div>
                            <div class="ai-agent">${user.ai}</div>
                        </div>
                    `;
                    // 绑定拖动逻辑(简单版)
                }
                container.appendChild(card);
            }
        }

        // 滑动控制
        function swipe(direction) {
            const topCard = container.querySelector(`.card[style*="z-index: 0"]`);
            if (!topCard) return;

            if (direction === 'right') {
                topCard.style.transform = 'translateX(150%) rotate(20deg)';
                setTimeout(() => {
                    document.getElementById('matchModal').style.display = 'flex';
                }, 300);
            } else {
                topCard.style.transform = 'translateX(-150%) rotate(-20deg)';
            }
            
            currentIndex++;
            setTimeout(renderCards, 400); // 动画结束后重绘
        }

        function closeMatch() {
            document.getElementById('matchModal').style.display = 'none';
        }

        // 主题切换
        function toggleTheme() {
            const body = document.body;
            const btn = document.querySelector('.theme-btn');
            if (body.getAttribute('data-theme') === 'light') {
                body.setAttribute('data-theme', 'dark');
                btn.innerText = '☀️';
            } else {
                body.setAttribute('data-theme', 'light');
                btn.innerText = '🌙';
            }
        }

        // 页面加载时初始化
        window.onload = renderCards;
    </script>
</body>
</html>
"""

# 高度设为 1000 以适配大部分桌面端屏幕
components.html(html_code, height=1000, scrolling=False)
