import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hometree", layout="wide", initial_sidebar_state="collapsed")
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
            --bg: #F5F5F7;
            --panel: #FFFFFF;
            --text: #1D1D1F;
            --sub: #86868B;
            --border: #E5E5EA;
            --accent: #FF69B4;
            --card-shadow: 0 10px 30px rgba(0,0,0,0.1);
            --douban: #007722;
            --netease: #C20C0C;
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

        .layout { display: flex; height: 100vh; width: 100vw; }
        
        /* 左侧导航 */
        .sidebar { width: 250px; border-right: 1px solid var(--border); padding: 20px; background: var(--panel); flex-shrink: 0; display: flex; flex-direction: column; }
        .logo { font-size: 24px; font-weight: 900; color: var(--accent); letter-spacing: -1px; margin-bottom: 30px;}
        .user-panel { display: flex; align-items: center; gap: 10px; margin-bottom: 30px; }
        .user-panel img { width: 50px; height: 50px; border-radius: 12px; border: 2px solid var(--accent); object-fit: cover;}
        .nav-item { padding: 12px 0; color: var(--sub); font-size: 14px; cursor: pointer; border-bottom: 1px dashed var(--border); display: flex; justify-content: space-between;}
        .nav-item:hover { color: var(--accent); }
        .nav-item.active { color: var(--accent); font-weight: bold; }

        /* 中间主区 */
        .main-feed { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; background: var(--bg); }
        
        /* 卡片堆叠区 */
        .card-container { width: 380px; height: 580px; position: relative; }
        .card { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: var(--panel); border-radius: 24px; border: 1px solid var(--border); box-shadow: var(--card-shadow); overflow: hidden; display: flex; flex-direction: column; transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), opacity 0.4s ease; }
        
        .card-img { width: 100%; height: 50%; object-fit: cover; }
        .card-content { padding: 20px; flex: 1; display: flex; flex-direction: column; }
        
        .name-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
        .name { font-size: 24px; font-weight: bold; }
        .tags { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 15px; }
        .tag { background: var(--bg); border: 1px solid var(--border); color: var(--accent); padding: 4px 10px; border-radius: 8px; font-size: 12px; }
        
        /* 豆瓣和网易云标识 */
        .media-links { display: flex; gap: 10px; margin-bottom: 15px; }
        .media-btn { padding: 4px 8px; border-radius: 4px; font-size: 11px; color: white; text-decoration: none; display: flex; align-items: center; gap: 4px; }
        .btn-douban { background-color: var(--douban); }
        .btn-netease { background-color: var(--netease); }

        .quote { font-size: 14px; color: var(--sub); font-style: italic; border-left: 2px solid var(--accent); padding-left: 10px; margin-bottom: 15px; }
        .ai-agent { font-size: 12px; color: var(--accent); font-family: monospace; margin-top: auto; background: var(--bg); padding: 10px; border-radius: 8px; }

        /* 操作按钮 */
        .controls { margin-top: 30px; display: flex; gap: 20px; }
        .btn { width: 65px; height: 65px; border-radius: 50%; border: 2px solid var(--border); background: var(--panel); color: var(--text); font-size: 24px; cursor: pointer; display: flex; justify-content: center; align-items: center; box-shadow: var(--card-shadow); transition: 0.2s; }
        .btn:hover { transform: scale(1.1); border-color: var(--accent); color: var(--accent); }
        .btn-like { width: 75px; height: 75px; font-size: 30px; border-color: var(--accent); color: var(--accent); }
        
        /* 顶部 */
        .top-nav { position: absolute; top: 20px; right: 20px; display: flex; gap: 10px; z-index: 100; }
        .theme-btn { width: 40px; height: 40px; border-radius: 50%; border: 1px solid var(--border); background: var(--panel); color: var(--text); cursor: pointer; display: flex; justify-content: center; align-items: center; font-size: 18px; box-shadow: var(--card-shadow); }
        
        /* 弹窗 */
        .modal { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: var(--panel); z-index: 1000; display: none; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 40px; }
        .modal h1 { color: var(--accent); font-size: 32px; margin-bottom: 20px; }
        .modal button { padding: 15px 30px; border-radius: 30px; background: var(--accent); color: #FFF; border: none; font-size: 16px; cursor: pointer; margin-top: 30px; }

        /* 侧边抽屉（书影音 & 设置） */
        .drawer { position: absolute; top: 0; left: 250px; height: 100%; width: 350px; background: var(--panel); border-right: 1px solid var(--border); z-index: 500; transform: translateX(-100%); transition: transform 0.3s; padding: 30px; overflow-y: auto; box-shadow: var(--card-shadow); }
        .drawer.open { transform: translateX(0); }
        .drawer-title { font-size: 20px; font-weight: bold; margin-bottom: 20px; border-bottom: 2px solid var(--accent); padding-bottom: 10px; display: inline-block;}
        
        .media-item { display: flex; gap: 15px; margin-bottom: 15px; padding-bottom: 15px; border-bottom: 1px solid var(--border); }
        .media-item img { width: 60px; height: 85px; object-fit: cover; border-radius: 4px; }
        .media-info h4 { font-size: 15px; margin-bottom: 5px; }
        .media-info p { font-size: 12px; color: var(--sub); }

        .setting-item { display: flex; justify-content: space-between; align-items: center; padding: 15px 0; border-bottom: 1px solid var(--border); font-size: 14px; }
        .toggle { width: 44px; height: 24px; background: var(--border); border-radius: 12px; position: relative; cursor: pointer; transition: 0.3s; }
        .toggle::after { content: ''; position: absolute; top: 2px; left: 2px; width: 20px; height: 20px; background: white; border-radius: 50%; transition: 0.3s; }
        .toggle.active { background: var(--accent); }
        .toggle.active::after { transform: translateX(20px); }
    </style>
</head>
<body data-theme="light">

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
            <div class="nav-item active" onclick="openDrawer('feedDrawer')"><span>📂 我的书影音</span></div>
            <div class="nav-item"><span>💬 匹配消息</span></div>
            <div class="nav-item" onclick="openDrawer('settingsDrawer')"><span>⚙ 隐私设置</span></div>
        </div>

        <!-- 抽屉：我的书影音 -->
        <div class="drawer" id="feedDrawer">
            <div class="drawer-title">My Tastes 我的书影音</div>
            <div style="margin-top: 20px;">
                <h4 style="color:var(--sub); font-size:12px; margin-bottom:10px;">Recently Read</h4>
                <div class="media-item">
                    <img src="https://img1.doubanio.com/view/subject/s/public/s27237850.jpg">
                    <div class="media-info"><h4>《百年孤独》</h4><p>马尔克斯</p></div>
                </div>
                <div class="media-item">
                    <img src="https://img9.doubanio.com/view/subject/s/public/s28385152.jpg">
                    <div class="media-info"><h4>《撒哈拉的故事》</h4><p>三毛</p></div>
                </div>
                <div class="media-item">
                    <img src="https://img9.doubanio.com/view/subject/s/public/s27310421.jpg">
                    <div class="media-info"><h4>《我的天才女友》</h4><p>埃莱娜·费兰特</p></div>
                </div>
                <div class="media-item">
                    <img src="https://img3.doubanio.com/view/subject/s/public/s33747736.jpg">
                    <div class="media-info"><h4>《正常人》</h4><p>萨莉·鲁尼</p></div>
                </div>
            </div>
        </div>

        <!-- 抽屉：隐私设置 -->
        <div class="drawer" id="settingsDrawer">
            <div class="drawer-title">Privacy & Settings</div>
            <div style="margin-top: 20px;">
                <div class="setting-item">
                    <span>隐身模式（不被推荐）</span>
                    <div class="toggle" onclick="this.classList.toggle('active')"></div>
                </div>
                <div class="setting-item">
                    <span>仅限通过豆瓣/网易云匹配</span>
                    <div class="toggle active" onclick="this.classList.toggle('active')"></div>
                </div>
                <div class="setting-item">
                    <span>屏蔽我的地理位置</span>
                    <div class="toggle active" onclick="this.classList.toggle('active')"></div>
                </div>
                <div class="setting-item">
                    <span>黑名单管理</span>
                    <span style="color:var(--accent); cursor:pointer;">2 人 ></span>
                </div>
            </div>
        </div>

        <!-- 中间区 -->
        <div class="main-feed">
            <div class="card-container" id="cardContainer"></div>
            <div class="controls">
                <button class="btn" onclick="swipe('left')">✕</button>
                <button class="btn btn-like" onclick="swipe('right')">♥</button>
            </div>
        </div>
    </div>

    <div class="modal" id="matchModal">
        <h1>FREQUENCY ALIGNED.</h1>
        <p>你们的精神频率已对齐。</p>
        <button onclick="closeMatch()">发送消息</button>
    </div>

    <script>
        const users = [
            { name: "娄烨", img: "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=500", tags: ["苏州河", "推拿"], quote: "如果有一天我走了，你会像马达那样找我吗？", ai: "AI: 适合在雨天聊贾宏声。" },
            { name: "Tyler Durden", img: "https://images.unsplash.com/photo-1520637836862-4d197d17c90a?w=500", tags: ["Fight Club", "Nihilism"], quote: "You are not your job.", ai: "AI: 别聊工作，聊地下搏击。" },
            { name: "The Smiths", img: "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?w=500", tags: ["Jangle Pop", "Morrissey"], quote: "There is a light that never goes out.", ai: "AI: 深夜 emo 必备。" },
            { name: "Björk", img: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=500", tags: ["Art Pop", "Homogenic"], quote: "I'm the spark.", ai: "AI: 冰岛极光与实验电子。" },
            { name: "罗大佑", img: "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=500", tags: ["鹿港小镇", "时代挽歌"], quote: "台北不是我的家。", ai: "AI: 午夜聊华语启蒙。" }
        ];

        let currentIndex = 0;
        const container = document.getElementById('cardContainer');

        function renderCards() {
            container.innerHTML = '';
            for (let i = users.length - 1; i >= 0; i--) {
                const user = users[i];
                const card = document.createElement('div');
                card.className = 'card';
                const offset = i - currentIndex;
                
                if (offset < 0) {
                    card.style.display = 'none';
                } else {
                    card.style.transform = `scale(${1 - offset * 0.05}) translateY(${offset * 10}px)`;
                    card.style.zIndex = -offset;
                    card.style.opacity = 1 - offset * 0.2;
                    
                    card.innerHTML = `
                        <img src="${user.img}" class="card-img">
                        <div class="card-content">
                            <div class="name-row"><div class="name">${user.name}</div></div>
                            <div class="tags">${user.tags.map(t => `<span class="tag">${t}</span>`).join('')}</div>
                            
                            <!-- 豆瓣 & 网易云 标识 -->
                            <div class="media-links">
                                <a href="#" class="media-btn btn-douban" onclick="alert('打开豆瓣详情：${user.tags[0]}')">豆瓣同步</a>
                                <a href="#" class="media-btn btn-netease" onclick="alert('打开网易云歌单：${user.tags[0]}')">网易云</a>
                            </div>

                            <div class="quote">"${user.quote}"</div>
                            <div class="ai-agent">${user.ai}</div>
                        </div>
                    `;
                }
                container.appendChild(card);
            }
        }

        function swipe(direction) {
            const topCard = container.querySelector(`.card[style*="z-index: 0"]`);
            if (!topCard) return;

            if (direction === 'right') {
                topCard.style.transform = 'translateX(150%) rotate(20deg)';
                setTimeout(() => { document.getElementById('matchModal').style.display = 'flex'; }, 300);
            } else {
                topCard.style.transform = 'translateX(-150%) rotate(-20deg)';
            }
            
            currentIndex++;
            setTimeout(renderCards, 400); 
        }

        function closeMatch() { document.getElementById('matchModal').style.display = 'none'; }

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

        // 侧边抽屉控制
        function openDrawer(id) {
            const drawers = document.querySelectorAll('.drawer');
            drawers.forEach(d => d.classList.remove('open'));
            document.getElementById(id).classList.add('open');
        }

        window.onload = renderCards;
    </script>
</body>
</html>
"""

components.html(html_code, height=1000, scrolling=False)
