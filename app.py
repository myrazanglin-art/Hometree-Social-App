import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hometree Extreme", layout="wide", initial_sidebar_state="collapsed")
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
            --border: #E5E5EA; --accent: #FF69B4; --card-shadow: 0 4px 12px rgba(0,0,0,0.1);
            --douban: #007722; --netease: #C20C0C; --ai-blue: #12B7F5;
        }
        [data-theme="dark"] {
            --bg: #121212; --panel: #1E1E1E; --text: #F2F2F7; --sub: #8E8E93;
            --border: #333333; --accent: #FF1493; --card-shadow: 0 4px 12px rgba(0,0,0,0.8);
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background: var(--bg); color: var(--text); height: 100vh; overflow: hidden; transition: background 0.3s; }

        /* 全局框架 */
        .app { display: flex; flex-direction: column; height: 100vh; }
        .top-bar { height: 50px; background: var(--panel); border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; padding: 0 20px; z-index: 100; }
        .logo { font-size: 20px; font-weight: 900; color: var(--accent); letter-spacing: -1px;}
        .content { flex: 1; overflow: hidden; position: relative; }

        /* 极繁页面 */
        .tab-page { display: none; height: 100%; overflow-y: auto; padding: 15px; }
        .tab-page.active { display: block; }

        /* 底部导航 */
        .bottom-nav { height: 60px; background: var(--panel); border-top: 1px solid var(--border); display: flex; justify-content: space-around; align-items: center; z-index: 100; }
        .nav-item { display: flex; flex-direction: column; align-items: center; font-size: 11px; color: var(--sub); cursor: pointer; }
        .nav-item.active { color: var(--accent); }
        .nav-icon { font-size: 22px; margin-bottom: 2px; }

        /* ================== 1. 匹配页 (极繁 Tinder) ================== */
        .match-layout { display: flex; gap: 20px; height: 100%; max-width: 900px; margin: 0 auto; }
        .deck-area { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        .card-container { width: 320px; height: 480px; position: relative; }
        
        .swipe-card { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: var(--panel); border-radius: 16px; border: 1px solid var(--border); box-shadow: var(--card-shadow); overflow: hidden; display: flex; flex-direction: column; transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); transform-origin: bottom center; }
        .card-img { width: 100%; height: 50%; object-fit: cover; }
        .card-info { padding: 12px; flex: 1; display: flex; flex-direction: column; background: linear-gradient(to bottom, var(--panel), #fafafa); }
        .name-row { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 6px; }
        .name { font-size: 20px; font-weight: bold; }
        .age { font-size: 13px; color: var(--sub); }
        .tags { display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 8px; }
        .tag { background: #FFF0F5; border: 1px solid #FFB6C1; color: var(--accent); padding: 2px 6px; border-radius: 4px; font-size: 10px; }
        .media-links { display: flex; gap: 6px; margin-bottom: 8px; }
        .media-btn { padding: 2px 6px; border-radius: 4px; font-size: 10px; color: white; cursor: pointer; }
        .btn-douban { background: var(--douban); }
        .btn-netease { background: var(--netease); }
        .quote { font-size: 12px; color: var(--sub); font-style: italic; border-left: 2px solid var(--accent); padding-left: 6px; margin-bottom: 8px; flex: 1;}
        .ai-agent { font-size: 11px; color: var(--ai-blue); font-family: monospace; background: rgba(18,183,245,0.05); padding: 6px; border-radius: 4px; border: 1px dashed var(--ai-blue); }
        
        .controls { margin-top: 20px; display: flex; gap: 20px; }
        .btn { width: 55px; height: 55px; border-radius: 50%; border: 1px solid var(--border); background: var(--panel); color: var(--text); font-size: 20px; cursor: pointer; display: flex; justify-content: center; align-items: center; box-shadow: var(--card-shadow); }
        .btn-like { width: 65px; height: 65px; color: var(--accent); border-color: var(--accent); font-size: 24px;}

        /* 右侧：已匹配列表 (常驻，极繁感) */
        .matches-sidebar { width: 250px; background: var(--panel); border: 1px solid var(--border); border-radius: 12px; padding: 15px; display: flex; flex-direction: column; overflow-y: auto; }
        .matches-title { font-size: 14px; font-weight: bold; margin-bottom: 15px; border-bottom: 1px solid var(--border); padding-bottom: 8px; }
        .match-item { display: flex; align-items: center; gap: 10px; padding: 10px; border-radius: 8px; cursor: pointer; transition: 0.2s; }
        .match-item:hover { background: var(--bg); }
        .match-avatar { width: 40px; height: 40px; border-radius: 50%; object-fit: cover; border: 2px solid var(--accent); }
        .match-info { flex: 1; overflow: hidden; }
        .match-name { font-size: 13px; font-weight: bold; }
        .match-last { font-size: 11px; color: var(--sub); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

        /* ================== 2. 书市 (多抓鱼极繁版) ================== */
        .market-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 15px; }
        .book-item { display: flex; gap: 12px; background: var(--panel); padding: 12px; border-radius: 12px; box-shadow: var(--card-shadow); border: 1px solid var(--border); }
        .book-cover { width: 70px; height: 100px; object-fit: cover; border-radius: 4px; }
        .book-info { flex: 1; display: flex; flex-direction: column;}
        .book-title { font-size: 14px; font-weight: bold; margin-bottom: 4px; }
        .book-meta { font-size: 11px; color: var(--sub); margin-bottom: 8px;}
        .book-price { color: #E65100; font-weight: bold; font-size: 14px; margin-top: auto;}
        .buy-btn { padding: 4px 8px; background: var(--accent); color: white; border: none; border-radius: 4px; font-size: 11px; cursor: pointer; float: right; margin-top: auto;}

        /* ================== 3. 社区 (小红书瀑布流) ================== */
        .xhs-masonry { column-count: 2; column-gap: 15px; }
        .xhs-card { background: var(--panel); border-radius: 12px; overflow: hidden; box-shadow: var(--card-shadow); margin-bottom: 15px; break-inside: avoid; border: 1px solid var(--border); }
        .xhs-img { width: 100%; object-fit: cover; }
        .xhs-content { padding: 10px; font-size: 13px; font-weight: bold; line-height: 1.4; }
        .xhs-author { display: flex; align-items: center; gap: 8px; padding: 0 10px 10px; font-size: 11px; color: var(--sub); }
        .xhs-avatar { width: 20px; height: 20px; border-radius: 50%; }

        /* ================== 4. 我的/隐私 ================== */
        .profile-header { background: var(--panel); padding: 20px; border-radius: 12px; display: flex; gap: 15px; align-items: center; margin-bottom: 20px; border: 1px solid var(--border);}
        .avatar { width: 70px; height: 70px; border-radius: 16px; object-fit: cover; border: 2px solid var(--accent); }
        .settings-grid { display: grid; grid-template-columns: 1fr; gap: 10px; }
        .setting-card { background: var(--panel); border-radius: 12px; padding: 15px; display: flex; justify-content: space-between; align-items: center; border: 1px solid var(--border); font-size: 14px;}
        .toggle { width: 40px; height: 22px; background: var(--border); border-radius: 11px; position: relative; cursor: pointer; }
        .toggle::after { content: ''; position: absolute; top: 2px; left: 2px; width: 18px; height: 18px; background: white; border-radius: 50%; transition: 0.3s; }
        .toggle.active { background: var(--accent); }
        .toggle.active::after { transform: translateX(18px); }

        /* ================== 5. 聊天弹窗 (持久化保存) ================== */
        .chat-modal { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: var(--panel); z-index: 1000; display: none; flex-direction: column; }
        .chat-header { padding: 15px; border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 10px; background: var(--panel); }
        .back-btn { background: none; border: none; font-size: 20px; cursor: pointer; color: var(--text); }
        .chat-avatar { width: 36px; height: 36px; border-radius: 50%; object-fit: cover; }
        .chat-name { font-size: 16px; font-weight: bold; }
        .chat-body { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; background: var(--bg); }
        .msg { max-width: 80%; padding: 10px 14px; border-radius: 16px; font-size: 14px; line-height: 1.4; }
        .msg-left { background: var(--panel); border: 1px solid var(--border); align-self: flex-start; border-bottom-left-radius: 2px; }
        .msg-right { background: var(--accent); color: white; align-self: flex-end; border-bottom-right-radius: 2px; }
        .chat-input-area { padding: 15px; border-top: 1px solid var(--border); display: flex; gap: 10px; background: var(--panel); }
        .chat-input { flex: 1; padding: 10px 15px; border-radius: 20px; border: 1px solid var(--border); background: var(--bg); color: var(--text); outline: none; }
        .send-btn { padding: 0 20px; border-radius: 20px; border: none; background: var(--accent); color: white; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body data-theme="light">

    <div class="app">
        <div class="top-bar">
            <div class="logo">HOMETREE. 🌸</div>
            <button class="theme-btn" onclick="toggleTheme()" style="background:none;border:none;font-size:18px;cursor:pointer;color:var(--text)">🌙 夜间模式</button>
        </div>

        <div class="content">
            <!-- 1. 匹配页 -->
            <div class="tab-page active" id="page-match">
                <div class="match-layout">
                    <div class="deck-area">
                        <div class="card-container" id="cardContainer"></div>
                        <div class="controls">
                            <button class="btn" onclick="swipe('left')">✕</button>
                            <button class="btn btn-like" onclick="swipe('right')">♥</button>
                        </div>
                    </div>
                    <!-- 右侧已匹配列表 -->
                    <div class="matches-sidebar">
                        <div class="matches-title">💬 匹配消息 ({matchesCount})</div>
                        <div id="matchesList">
                            <!-- JS 动态渲染 -->
                        </div>
                    </div>
                </div>
            </div>

            <!-- 2. 书市页 -->
            <div class="tab-page" id="page-market">
                <h2 style="margin-bottom:15px; font-size:18px;">多抓鱼书市 (二手漂流)</h2>
                <div class="market-grid">
                    <div class="book-item">
                        <img src="https://img9.doubanio.com/view/subject/s/public/s28385152.jpg" class="book-cover">
                        <div class="book-info">
                            <div class="book-title">撒哈拉的故事</div>
                            <div class="book-meta">三毛 | 9成新 | 北京</div>
                            <div class="book-price">¥ 12.00 <button class="buy-btn">加入书袋</button></div>
                        </div>
                    </div>
                    <div class="book-item">
                        <img src="https://img9.doubanio.com/view/subject/s/public/s27310421.jpg" class="book-cover">
                        <div class="book-info">
                            <div class="book-title">我的天才女友</div>
                            <div class="book-meta">费兰特 | 8成新 | 上海</div>
                            <div class="book-price">¥ 18.50 <button class="buy-btn">加入书袋</button></div>
                        </div>
                    </div>
                    <div class="book-item">
                        <img src="https://img3.doubanio.com/view/subject/s/public/s33747736.jpg" class="book-cover">
                        <div class="book-info">
                            <div class="book-title">正常人</div>
                            <div class="book-meta">萨莉·鲁尼 | 全新 | 广州</div>
                            <div class="book-price">¥ 25.00 <button class="buy-btn">加入书袋</button></div>
                        </div>
                    </div>
                    <div class="book-item">
                        <img src="https://img1.doubanio.com/view/subject/s/public/s27237850.jpg" class="book-cover">
                        <div class="book-info">
                            <div class="book-title">百年孤独</div>
                            <div class="book-meta">马尔克斯 | 7成新 | 杭州</div>
                            <div class="book-price">¥ 9.90 <button class="buy-btn">加入书袋</button></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 3. 社区页 -->
            <div class="tab-page" id="page-community">
                <h2 style="margin-bottom:15px; font-size:18px;">精神自留地</h2>
                <div class="xhs-masonry">
                    <div class="xhs-card">
                        <img src="https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=400" class="xhs-img" style="height:250px;">
                        <div class="xhs-content">罗大佑的歌词，句句都是时代挽歌。</div>
                        <div class="xhs-author"><img src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=50" class="xhs-avatar"> Yiming</div>
                    </div>
                    <div class="xhs-card">
                        <img src="https://images.unsplash.com/photo-1520637836862-4d197d17c90a?w=400" class="xhs-img" style="height:180px;">
                        <div class="xhs-content">重看《搏击俱乐部》，还是被 Tyler 震撼。</div>
                        <div class="xhs-author"><img src="https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=50" class="xhs-avatar"> 娄烨</div>
                    </div>
                    <div class="xhs-card">
                        <img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=400" class="xhs-img" style="height:220px;">
                        <div class="xhs-content">Björk 的现场是一场极光祭祀。</div>
                        <div class="xhs-author"><img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=50" class="xhs-avatar"> Björk</div>
                    </div>
                </div>
            </div>

            <!-- 4. 我的页 -->
            <div class="tab-page" id="page-profile">
                <div class="profile-header">
                    <img src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=200" class="avatar">
                    <div>
                        <h2 style="font-size:18px;">Yiming</h2>
                        <p style="font-size:12px;color:var(--sub); margin-top:5px;">豆瓣 126本在读 | 网易云 89首私藏</p>
                    </div>
                </div>
                <div class="settings-grid">
                    <div class="setting-card">
                        <span>🔒 隐身模式 (不被推荐)</span>
                        <div class="toggle active" onclick="this.classList.toggle('active')"></div>
                    </div>
                    <div class="setting-card">
                        <span>🚫 屏蔽/拉黑管理</span>
                        <span style="color:var(--accent); cursor:pointer;">查看 (2)</span>
                    </div>
                    <div class="setting-card">
                        <span>📚 同步豆瓣书影音</span>
                        <span style="color:var(--accent); cursor:pointer;">已绑定</span>
                    </div>
                    <div class="setting-card">
                        <span>🎵 同步网易云歌单</span>
                        <span style="color:var(--sub); cursor:pointer;">未绑定</span>
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
        <div class="chat-input-area">
            <input class="chat-input" id="chatInput" placeholder="发消息..." onkeypress="if(event.key === 'Enter') sendMessage()">
            <button class="send-btn" onclick="sendMessage()">发送</button>
        </div>
    </div>

    <script>
        // ================= 1. 数据配置 =================
        const users = [
            { id: "louye", name: "娄烨", age: 58, img: "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=600", tags: ["苏州河", "推拿"], quote: "如果有一天我走了...", ai: "AI: 适合在雨天聊贾宏声。" },
            { id: "tyler", name: "Tyler Durden", age: 30, img: "https://images.unsplash.com/photo-1520637836862-4d197d17c90a?w=600", tags: ["Fight Club", "Nihilism"], quote: "You are not your job.", ai: "AI: 别聊工作，聊地下搏击。" },
            { id: "morrissey", name: "Morrissey", age: 64, img: "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?w=600", tags: ["The Smiths", "Indie"], quote: "There is a light...", ai: "AI: 深夜 emo 必备。" },
            { id: "bjork", name: "Björk", age: 58, img: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600", tags: ["Art Pop", "实验电子"], quote: "I'm the spark.", ai: "AI: 冰岛极光与实验电子。" },
            { id: "lotayu", name: "罗大佑", age: 68, img: "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=600", tags: ["鹿港小镇", "时代"], quote: "台北不是我的家。", ai: "AI: 午夜聊华语启蒙。" },
            { id: "emo", name: "Midwest Emo", age: 22, img: "https://images.unsplash.com/photo-1501386761578-eac5c94b800a?w=600", tags: ["Math Rock", "Drop D"], quote: "Let's play in drop D.", ai: "AI: 效果器男孩。" },
            { id: "muse", name: "Matt Bellamy", age: 45, img: "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=600", tags: ["Muse", "Space Rock"], quote: "This is the last time.", ai: "AI: 科幻与反乌托邦。" },
            { id: "aphex", name: "Aphex Twin", age: 52, img: "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=600", tags: ["IDM", "Ambient"], quote: "Weird music.", ai: "AI: Max/MSP 同好。" },
            { id: "kurt", name: "Kurt Cobain", age: 27, img: "https://images.unsplash.com/photo-1520637836862-4d197d17c90a?w=600", tags: ["Grunge", "Nirvana"], quote: "I'd rather be hated.", ai: "AI: 聊聊地下厂牌。" },
            { id: "kevin", name: "Kevin Shields", age: 60, img: "https://images.unsplash.com/photo-1516280440502-863a346513c1?w=600", tags: ["Shoegaze", "MBV"], quote: "Loveless is a wall.", ai: "AI: 噪音墙之神。" }
        ];

        // 全局状态存储
        let currentIndex = 0;
        let matchedUsers = JSON.parse(localStorage.getItem('hometree_matches')) || [];
        let chatHistories = JSON.parse(localStorage.getItem('hometree_chats')) || {};
        let activeChatId = null;
        
        const container = document.getElementById('cardContainer');

        // ================= 2. 渲染卡片与列表 =================
        function renderAll() {
            // 渲染卡片
            container.innerHTML = '';
            if (currentIndex >= users.length) {
                container.innerHTML = '<div style="text-align:center;color:var(--sub);margin-top:200px;">没有更多推荐了</div>';
            } else {
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
                                <span class="media-btn btn-douban" onclick="event.stopPropagation(); alert('跳转豆瓣查看：${user.tags[0]}')">豆瓣</span>
                                <span class="media-btn btn-netease" onclick="event.stopPropagation(); alert('跳转网易云查看：${user.tags[0]}')">网易云</span>
                            </div>
                            <div class="quote">"${user.quote}"</div>
                            <div class="ai-agent">🤖 ${user.ai}</div>
                        </div>
                    `;
                    container.appendChild(card);
                }
            }

            // 渲染右侧匹配列表
            document.querySelector('.matches-title').innerHTML = `💬 匹配消息 (${matchedUsers.length})`;
            const list = document.getElementById('matchesList');
            list.innerHTML = '';
            if(matchedUsers.length === 0) {
                list.innerHTML = '<div style="font-size:12px; color:var(--sub); text-align:center; margin-top:20px;">划动卡片匹配他们吧</div>';
            }
            matchedUsers.forEach(u => {
                const lastMsg = chatHistories[u.id] && chatHistories[u.id].length > 0 ? chatHistories[u.id].slice(-1)[0].text : "匹配成功，打个招呼吧！";
                const item = document.createElement('div');
                item.className = 'match-item';
                item.onclick = () => openChat(u);
                item.innerHTML = `
                    <img src="${u.img}" class="match-avatar">
                    <div class="match-info">
                        <div class="match-name">${u.name}</div>
                        <div class="match-last">${lastMsg}</div>
                    </div>
                `;
                list.appendChild(item);
            });
        }

        // ================= 3. 滑动与持久化 =================
        function swipe(direction) {
            if (currentIndex >= users.length) return;
            const topCard = container.querySelector(`.swipe-card[style*="z-index: 0"]`);
            if (!topCard) return;

            const user = users[currentIndex];

            if (direction === 'right') {
                topCard.style.transform = 'translateX(150%) rotate(20deg)';
                setTimeout(() => {
                    // 添加到匹配列表并持久化
                    if (!matchedUsers.find(u => u.id === user.id)) {
                        matchedUsers.push(user);
                        if(!chatHistories[user.id]) chatHistories[user.id] = [];
                        saveState();
                    }
                    openChat(user); // 直接打开聊天
                    renderAll(); // 更新UI
                }, 300);
            } else {
                topCard.style.transform = 'translateX(-150%) rotate(-20deg)';
            }
            currentIndex++;
            setTimeout(renderAll, 350); 
        }

        // ================= 4. 聊天系统 (带 localStorage 存储) =================
        function openChat(user) {
            activeChatId = user.id;
            document.getElementById('chatName').innerText = user.name;
            document.getElementById('chatAvatar').src = user.img;
            document.getElementById('chatModal').style.display = 'flex';
            renderChatMessages();
        }

        function closeChat() { 
            document.getElementById('chatModal').style.display = 'none'; 
            activeChatId = null;
            renderAll(); // 刷新右侧列表最新消息预览
        }

        function renderChatMessages() {
            const body = document.getElementById('chatBody');
            body.innerHTML = '';
            const msgs = chatHistories[activeChatId] || [];
            
            if (msgs.length === 0) {
                // 第一次聊，加个默认开场
                const user = users.find(u => u.id === activeChatId);
                addMessageToDB(activeChatId, `Hey，很高兴匹配到你。`, 'left');
                renderChatMessages();
                return;
            }

            msgs.forEach(m => {
                const div = document.createElement('div');
                div.className = `msg msg-${m.type}`;
                div.innerText = m.text;
                body.appendChild(div);
            });
            body.scrollTop = body.scrollHeight;
        }

        function addMessageToDB(id, text, type) {
            if(!chatHistories[id]) chatHistories[id] = [];
            chatHistories[id].push({ text, type });
            saveState();
            if(activeChatId === id) renderChatMessages();
        }

        function sendMessage() {
            const input = document.getElementById('chatInput');
            if (input.value.trim() !== '' && activeChatId) {
                addMessageToDB(activeChatId, input.value, 'right');
                input.value = '';
                // 模拟回复
                setTimeout(() => {
                    addMessageToDB(activeChatId, "我也这么觉得，这就是我们在这里相遇的原因。", 'left');
                }, 1000);
            }
        }

        // 数据存储到浏览器
        function saveState() {
            localStorage.setItem('hometree_matches', JSON.stringify(matchedUsers));
            localStorage.setItem('hometree_chats', JSON.stringify(chatHistories));
            renderAll();
        }

        // ================= 5. UI 切换 =================
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

        window.onload = renderAll;
    </script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=False)
