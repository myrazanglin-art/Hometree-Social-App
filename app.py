import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hometree Super App", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
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
        :root {
            --bg: #F5F5F7; --panel: #FFFFFF; --text: #1D1D1F; --sub: #86868B;
            --border: #E5E5EA; --accent: #FF69B4; --card-shadow: 0 10px 20px rgba(0,0,0,0.1);
            --douban: #007722; --netease: #C20C0C; --ai-blue: #12B7F5;
        }
        [data-theme="dark"] {
            --bg: #121212; --panel: #1E1E1E; --text: #F2F2F7; --sub: #8E8E93;
            --border: #333333; --accent: #FF1493; --card-shadow: 0 10px 20px rgba(0,0,0,0.8);
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background: var(--bg); color: var(--text); height: 100vh; overflow: hidden; transition: background 0.3s; }

        /* 全局结构 */
        .app { display: flex; flex-direction: column; height: 100vh; }
        .top-bar { height: 50px; background: var(--panel); border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; padding: 0 20px; z-index: 10; }
        .logo { font-size: 20px; font-weight: 900; color: var(--accent); }
        .content { flex: 1; overflow-y: auto; position: relative; }
        .tab-page { display: none; padding: 20px; height: 100%; }
        .tab-page.active { display: block; }

        /* 底部导航 */
        .bottom-nav { height: 60px; background: var(--panel); border-top: 1px solid var(--border); display: flex; justify-content: space-around; align-items: center; z-index: 100; }
        .nav-item { display: flex; flex-direction: column; align-items: center; font-size: 11px; color: var(--sub); cursor: pointer; }
        .nav-item.active { color: var(--accent); }
        .nav-icon { font-size: 22px; margin-bottom: 2px; }

        /* ====== 1. 匹配页 (Tinder) ====== */
        .match-wrapper { height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; }
        .card-container { width: 320px; height: 480px; position: relative; }
        .swipe-card { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: var(--panel); border-radius: 20px; border: 1px solid var(--border); box-shadow: var(--card-shadow); overflow: hidden; display: flex; flex-direction: column; transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); transform-origin: bottom center; }
        .card-img { width: 100%; height: 55%; object-fit: cover; }
        .card-info { padding: 15px; flex: 1; display: flex; flex-direction: column; }
        .name-row { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 5px; }
        .name { font-size: 22px; font-weight: bold; }
        .tags { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 10px; }
        .tag { background: var(--bg); border: 1px solid var(--border); color: var(--accent); padding: 2px 8px; border-radius: 12px; font-size: 11px; }
        .media-links { display: flex; gap: 5px; margin-bottom: 10px; }
        .media-btn { padding: 2px 6px; border-radius: 4px; font-size: 10px; color: white; text-decoration: none; cursor: pointer; }
        .btn-douban { background: var(--douban); }
        .btn-netease { background: var(--netease); }
        .quote { font-size: 12px; color: var(--sub); font-style: italic; border-left: 2px solid var(--accent); padding-left: 8px; margin-bottom: 10px; flex: 1; }
        .ai-agent { font-size: 11px; color: var(--ai-blue); font-family: monospace; background: rgba(18,183,245,0.1); padding: 8px; border-radius: 6px; border: 1px dashed var(--ai-blue); }
        
        .controls { margin-top: 20px; display: flex; gap: 20px; }
        .btn { width: 60px; height: 60px; border-radius: 50%; border: 1px solid var(--border); background: var(--panel); color: var(--text); font-size: 24px; cursor: pointer; display: flex; justify-content: center; align-items: center; box-shadow: var(--card-shadow); }
        .btn-like { width: 70px; height: 70px; color: var(--accent); border-color: var(--accent); }

        /* ====== 2. 书市 (多抓鱼风) ====== */
        .book-grid { display: grid; grid-template-columns: 1fr; gap: 15px; }
        .book-item { display: flex; gap: 15px; background: var(--panel); padding: 15px; border-radius: 12px; box-shadow: var(--card-shadow); }
        .book-cover { width: 80px; height: 110px; object-fit: cover; border-radius: 4px; }
        .book-info { flex: 1; }
        .book-title { font-size: 16px; font-weight: bold; margin-bottom: 5px; }
        .book-author { font-size: 12px; color: var(--sub); }
        .book-price { color: #E65100; font-weight: bold; margin-top: 5px; }
        .buy-btn { padding: 5px 10px; background: var(--accent); color: white; border: none; border-radius: 4px; font-size: 12px; cursor: pointer; float: right; }

        /* ====== 3. 社区 (小红书风) ====== */
        .xhs-grid { display: grid; grid-template-columns: 1fr; gap: 15px; }
        .xhs-post { background: var(--panel); border-radius: 12px; overflow: hidden; box-shadow: var(--card-shadow); }
        .xhs-img { width: 100%; height: 200px; object-fit: cover; }
        .xhs-text { padding: 10px; font-size: 13px; font-weight: bold; }

        /* ====== 4. 我的与隐私 ====== */
        .profile-box { background: var(--panel); padding: 20px; border-radius: 12px; margin-bottom: 20px; text-align: center; }
        .avatar { width: 80px; height: 80px; border-radius: 50%; border: 3px solid var(--accent); object-fit: cover; margin-bottom: 10px; }
        .sync-text { font-size: 12px; color: var(--sub); margin-top: 5px; }
        .settings-box { background: var(--panel); border-radius: 12px; padding: 15px; }
        .setting-row { display: flex; justify-content: space-between; padding: 15px 0; border-bottom: 1px solid var(--border); }
        .setting-row:last-child { border-bottom: none; }
        .toggle { width: 40px; height: 20px; background: var(--border); border-radius: 10px; position: relative; cursor: pointer; }
        .toggle::after { content: ''; position: absolute; top: 2px; left: 2px; width: 16px; height: 16px; background: white; border-radius: 50%; transition: 0.3s; }
        .toggle.active { background: var(--accent); }
        .toggle.active::after { transform: translateX(20px); }

        /* ====== 聊天弹窗 ====== */
        .chat-modal { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: var(--panel); z-index: 1000; display: none; flex-direction: column; }
        .chat-header { padding: 15px 20px; border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 10px; }
        .back-btn { background: none; border: none; font-size: 20px; cursor: pointer; color: var(--text); margin-right: 10px; }
        .chat-avatar { width: 40px; height: 40px; border-radius: 50%; object-fit: cover; }
        .chat-name { font-size: 16px; font-weight: bold; }
        .chat-body { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }
        .msg { max-width: 80%; padding: 10px 15px; border-radius: 18px; font-size: 14px; }
        .msg-left { background: var(--bg); align-self: flex-start; border-bottom-left-radius: 4px; }
        .msg-right { background: var(--accent); color: white; align-self: flex-end; border-bottom-right-radius: 4px; }
        .ai-suggest-box { padding: 10px 20px; }
        .ai-suggest-btn { width: 100%; padding: 10px; background: rgba(18,183,245,0.1); color: var(--ai-blue); border: 1px dashed var(--ai-blue); border-radius: 8px; cursor: pointer; font-size: 12px; text-align: center; }
        .chat-input-area { padding: 15px; border-top: 1px solid var(--border); display: flex; gap: 10px; }
        .chat-input { flex: 1; padding: 10px; border-radius: 20px; border: 1px solid var(--border); background: var(--bg); color: var(--text); outline: none; }
        .send-btn { padding: 0 20px; border-radius: 20px; border: none; background: var(--accent); color: white; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body data-theme="light">

    <div class="app">
        <!-- 顶部栏 -->
        <div class="top-bar">
            <div class="logo">HOMETREE.</div>
            <button class="theme-btn" onclick="toggleTheme()" style="background:none;border:none;font-size:18px;cursor:pointer;color:var(--text)">🌙</button>
        </div>

        <!-- 内容区 -->
        <div class="content">
            <!-- 匹配页 -->
            <div class="tab-page active" id="page-match">
                <div class="match-wrapper">
                    <div class="card-container" id="cardContainer"></div>
                    <div class="controls">
                        <button class="btn" onclick="swipe('left')">✕</button>
                        <button class="btn btn-like" onclick="swipe('right')">♥</button>
                    </div>
                </div>
            </div>

            <!-- 书市页 -->
            <div class="tab-page" id="page-market">
                <h2 style="margin-bottom:15px;">多抓鱼书市</h2>
                <div class="book-grid">
                    <div class="book-item">
                        <img src="https://img9.doubanio.com/view/subject/s/public/s28385152.jpg" class="book-cover">
                        <div class="book-info">
                            <div class="book-title">撒哈拉的故事</div>
                            <div class="book-author">三毛 | 9成新</div>
                            <div class="book-price">¥ 12.00 <button class="buy-btn">加入书袋</button></div>
                        </div>
                    </div>
                    <div class="book-item">
                        <img src="https://img9.doubanio.com/view/subject/s/public/s27310421.jpg" class="book-cover">
                        <div class="book-info">
                            <div class="book-title">我的天才女友</div>
                            <div class="book-author">费兰特 | 8成新</div>
                            <div class="book-price">¥ 18.50 <button class="buy-btn">加入书袋</button></div>
                        </div>
                    </div>
                    <div class="book-item">
                        <img src="https://img3.doubanio.com/view/subject/s/public/s33747736.jpg" class="book-cover">
                        <div class="book-info">
                            <div class="book-title">正常人</div>
                            <div class="book-author">萨莉·鲁尼 | 全新</div>
                            <div class="book-price">¥ 25.00 <button class="buy-btn">加入书袋</button></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 社区页 -->
            <div class="tab-page" id="page-community">
                <h2 style="margin-bottom:15px;">精神自留地</h2>
                <div class="xhs-grid">
                    <div class="xhs-post">
                        <img src="https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=500" class="xhs-img">
                        <div class="xhs-text">罗大佑的歌词，句句都是时代挽歌。</div>
                    </div>
                    <div class="xhs-post">
                        <img src="https://images.unsplash.com/photo-1520637836862-4d197d17c90a?w=500" class="xhs-img">
                        <div class="xhs-text">重看《搏击俱乐部》，还是被 Tyler 震撼。</div>
                    </div>
                </div>
            </div>

            <!-- 我的页 -->
            <div class="tab-page" id="page-profile">
                <div class="profile-box">
                    <img src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=200" class="avatar">
                    <h2>Yiming</h2>
                    <div class="sync-text">已同步：豆瓣 126本在读 | 网易云 89首私藏</div>
                </div>
                <div class="settings-box">
                    <div class="setting-row">
                        <span>隐身模式</span>
                        <div class="toggle" onclick="this.classList.toggle('active')"></div>
                    </div>
                    <div class="setting-row">
                        <span>黑名单管理</span>
                        <span style="color:var(--accent); cursor:pointer;">查看 (2)</span>
                    </div>
                    <div class="setting-row">
                        <span>退出登录</span>
                        <span style="color:red; cursor:pointer;">退出</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- 底部导航 -->
        <div class="bottom-nav">
            <div class="nav-item active" onclick="switchTab('page-match', this)"><span class="nav-icon">🔥</span><span>匹配</span></div>
            <div class="nav-item" onclick="switchTab('page-market', this)"><span class="nav-icon">📚</span><span>书市</span></div>
            <div class="nav-item" onclick="switchTab('page-community', this)"><span class="nav-icon">🌸</span><span>社区</span></div>
            <div class="nav-item" onclick="switchTab('page-profile', this)"><span class="nav-icon">👤</span><span>我的</span></div>
        </div>
    </div>

    <!-- 聊天弹窗 -->
    <div class="chat-modal" id="chatModal">
        <div class="chat-header">
            <button class="back-btn" onclick="closeChat()">←</button>
            <img id="chatAvatar" class="chat-avatar" src="">
            <div class="chat-name" id="chatName"></div>
        </div>
        <div class="chat-body" id="chatBody"></div>
        <div class="ai-suggest-box">
            <div class="ai-suggest-btn" onclick="useAISuggest()">💡 AI Agent 破冰：点击生成专属开场白</div>
        </div>
        <div class="chat-input-area">
            <input class="chat-input" id="chatInput" placeholder="发消息...">
            <button class="send-btn" onclick="sendMessage()">发送</button>
        </div>
    </div>

    <script>
        // ================= 1. 数据配置 =================
        const users = [
            { name: "娄烨", age: 58, img: "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=600", tags: ["苏州河", "推拿", "第六代"], quote: "如果有一天我走了，你会像马达那样找我吗？", ai: "AI: 适合在雨天聊贾宏声。", opening: "你更喜欢《苏州河》里的马达，还是《推拿》里的小马？" },
            { name: "Tyler Durden", age: 30, img: "https://images.unsplash.com/photo-1520637836862-4d197d17c90a?w=600", tags: ["Fight Club", "虚无主义"], quote: "You are not your job.", ai: "AI: 别聊工作，聊地下搏击。", opening: "你觉得现代消费主义最恶心的一点是什么？" },
            { name: "Morrissey", age: 64, img: "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?w=600", tags: ["The Smiths", "Jangle Pop"], quote: "There is a light that never goes out.", ai: "AI: 深夜 emo 必备。", opening: "如果那辆双层巴士真的撞过来，你会放哪首歌？" },
            { name: "Björk", age: 58, img: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600", tags: ["Art Pop", "实验电子"], quote: "I'm carried by the storm.", ai: "AI: 冰岛极光与实验电子。", opening: "你的音乐里有一种冰川碎裂的声音，最近在听什么实验电子？" },
            { name: "罗大佑", age: 68, img: "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=600", tags: ["鹿港小镇", "时代挽歌"], quote: "台北不是我的家。", ai: "AI: 午夜聊华语启蒙。", opening: "你觉得现在的华语乐坛，还有人在写《鹿港小镇》这样的歌吗？" },
            { name: "Emo Kid", age: 22, img: "https://images.unsplash.com/photo-1501386761578-eac5c94b800a?w=600", tags: ["Midwest Emo", "Math Rock"], quote: "Let's play in drop D.", ai: "AI: 延迟效果器男孩。", opening: "你最喜欢 American Football 同名专辑里的哪一首？" },
            { name: "Matt Bellamy", age: 45, img: "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=600", tags: ["Muse", "Space Rock"], quote: "This is the last time.", ai: "AI: 科幻与反乌托邦。", opening: "如果世界即将毁灭，你会用哪首 Muse 的歌作为BGM？" },
            { name: "Aphex Twin", age: 52, img: "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=600", tags: ["IDM", "Ambient"], quote: "Weird music for weird people.", ai: "AI: Max/MSP 同好。", opening: "Windowlicker 里的碎拍，你到底是怎么切出来的？" },
            { name: "Kurt Cobain", age: 27, img: "https://images.unsplash.com/photo-1520637836862-4d197d17c90a?w=600", tags: ["Nirvana", "Grunge"], quote: "I'd rather be hated for who I am.", ai: "AI: 聊聊地下厂牌。", opening: "如果你还在，你会怎么看待现在的短视频神曲？" },
            { name: "Kevin Shields", age: 60, img: "https://images.unsplash.com/photo-1516280440502-863a346513c1?w=600", tags: ["Shoegaze", "MBV"], quote: "Loveless is a wall of sound.", ai: "AI: 噪音墙之神。", opening: "Loveless 这张专辑，你花了多久才听出里面的旋律？" }
        ];

        let currentIndex = 0;
        let currentMatch = null;
        const container = document.getElementById('cardContainer');

        // ================= 2. 渲染与滑动 =================
        function renderCards() {
            container.innerHTML = '';
            for (let i = users.length - 1; i >= 0; i--) {
                if (i < currentIndex) continue;
                const user = users[i];
                const card = document.createElement('div');
                card.className = 'swipe-card';
                const offset = i - currentIndex;
                card.style.transform = `scale(${1 - offset * 0.04}) translateY(${offset * 15}px)`;
                card.style.zIndex = -offset;
                card.style.opacity = 1 - offset * 0.15;
                
                card.innerHTML = `
                    <img src="${user.img}" class="card-img">
                    <div class="card-info">
                        <div class="name-row"><div class="name">${user.name}</div><div class="age">${user.age}</div></div>
                        <div class="tags">${user.tags.map(t => `<span class="tag">${t}</span>`).join('')}</div>
                        <div class="media-links">
                            <span class="media-btn btn-douban" onclick="event.stopPropagation(); alert('跳转豆瓣查看：${user.tags[0]}')">豆瓣同步</span>
                            <span class="media-btn btn-netease" onclick="event.stopPropagation(); alert('跳转网易云查看：${user.tags[0]}')">网易云</span>
                        </div>
                        <div class="quote">"${user.quote}"</div>
                        <div class="ai-agent">🤖 ${user.ai}</div>
                    </div>
                `;
                container.appendChild(card);
            }
        }

        function swipe(direction) {
            const topCard = container.querySelector(`.swipe-card[style*="z-index: 0"]`);
            if (!topCard) return;

            currentMatch = users[currentIndex];

            if (direction === 'right') {
                topCard.style.transform = 'translateX(150%) rotate(20deg)';
                setTimeout(() => { openChat(currentMatch); }, 300);
            } else {
                topCard.style.transform = 'translateX(-150%) rotate(-20deg)';
            }
            currentIndex++;
            setTimeout(renderCards, 350); 
        }

        // ================= 3. 聊天系统 =================
        function openChat(user) {
            document.getElementById('chatName').innerText = user.name;
            document.getElementById('chatAvatar').src = user.img;
            document.getElementById('chatBody').innerHTML = ''; 
            document.getElementById('chatModal').style.display = 'flex';
            setTimeout(() => {
                addMessage(`Hey，很高兴在这个频率遇见你。`, 'left');
            }, 600);
        }

        function closeChat() { document.getElementById('chatModal').style.display = 'none'; }

        function addMessage(text, type) {
            const chatBox = document.getElementById('chatBody');
            const msg = document.createElement('div');
            msg.className = `msg msg-${type}`;
            msg.innerText = text;
            chatBox.appendChild(msg);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function sendMessage() {
            const input = document.getElementById('chatInput');
            if (input.value.trim() !== '') {
                addMessage(input.value, 'right');
                input.value = '';
            }
        }

        function useAISuggest() {
            if(currentMatch) {
                addMessage(currentMatch.opening, 'right');
            }
        }

        // ================= 4. 页面与主题切换 =================
        function switchTab(pageId, btnElement) {
            document.querySelectorAll('.tab-page').forEach(p => p.classList.remove('active'));
            document.getElementById(pageId).classList.add('active');
            document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
            btnElement.classList.add('active');
        }

        function toggleTheme() {
            const body = document.body;
            body.setAttribute('data-theme', body.getAttribute('data-theme') === 'light' ? 'dark' : 'light');
        }

        window.onload = renderCards;
    </script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=False)
