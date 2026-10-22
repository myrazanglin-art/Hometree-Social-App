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
            --card-shadow: 0 10px 20px rgba(0,0,0,0.1);
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
            --card-shadow: 0 10px 20px rgba(0,0,0,0.8);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background: var(--bg); color: var(--text); height: 100vh; overflow: hidden; transition: background 0.3s; }

        /* 顶部导航 */
        .top-bar { height: 50px; background: var(--panel); border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; padding: 0 20px; position: relative; z-index: 100;}
        .logo { font-size: 20px; font-weight: 900; color: var(--accent); }
        .theme-btn { cursor: pointer; font-size: 18px; background:none; border:none; color:var(--text);}

        /* 页面容器 */
        .page { display: none; height: calc(100vh - 120px); overflow-y: auto; padding: 20px; }
        .page.active { display: block; }
        
        /* ============ 1. 匹配区 (带物理滑动的卡片) ============ */
        .match-wrapper { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; position: relative;}
        
        .card-container { width: 340px; height: 520px; position: relative; }
        
        .swipe-card { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: var(--panel); border-radius: 20px; border: 1px solid var(--border); box-shadow: var(--card-shadow); overflow: hidden; display: flex; flex-direction: column; transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), opacity 0.4s; transform-origin: bottom center;}
        
        .card-img { width: 100%; height: 60%; object-fit: cover; }
        .card-content { padding: 15px; flex: 1; display: flex; flex-direction: column; }
        .name-row { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 5px; }
        .name { font-size: 22px; font-weight: bold; }
        .age { font-size: 14px; color: var(--sub); }
        
        .tags { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 10px; }
        .tag { background: var(--bg); border: 1px solid var(--border); color: var(--accent); padding: 3px 8px; border-radius: 4px; font-size: 11px; }
        
        .media-links { display: flex; gap: 8px; margin-bottom: 10px; }
        .media-btn { padding: 3px 6px; border-radius: 4px; font-size: 10px; color: white; text-decoration: none; }
        .btn-douban { background-color: var(--douban); }
        .btn-netease { background-color: var(--netease); }

        .quote { font-size: 13px; color: var(--sub); font-style: italic; border-left: 2px solid var(--accent); padding-left: 8px; margin-bottom: 10px; }
        .ai-agent { font-size: 11px; color: var(--accent); font-family: monospace; margin-top: auto; background: var(--bg); padding: 8px; border-radius: 6px; }

        /* 操作按钮 */
        .controls { margin-top: 20px; display: flex; gap: 20px; }
        .btn { width: 60px; height: 60px; border-radius: 50%; border: 1px solid var(--border); background: var(--panel); color: var(--text); font-size: 24px; cursor: pointer; display: flex; justify-content: center; align-items: center; box-shadow: var(--card-shadow); transition: 0.2s; }
        .btn:hover { transform: scale(1.1); border-color: var(--accent); }
        .btn-like { width: 70px; height: 70px; color: var(--accent); border-color: var(--accent); }

        /* ============ 2. 多抓鱼二手书市 ============ */
        .market-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
        .book-item { background: var(--panel); border-radius: 12px; padding: 15px; box-shadow: var(--card-shadow); display: flex; gap: 15px; }
        .book-cover { width: 80px; height: 110px; object-fit: cover; border-radius: 4px; }
        .book-info h3 { font-size: 16px; margin-bottom: 5px;}
        .book-price { color: #E65100; font-weight: bold; font-size: 14px; margin-top: 5px;}
        .buy-btn { margin-top: 10px; padding: 5px 10px; background: var(--accent); color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 12px;}

        /* ============ 3. 小红书社区 ============ */
        .xhs-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 15px; }
        .xhs-post { background: var(--panel); border-radius: 12px; overflow: hidden; box-shadow: var(--card-shadow); cursor: pointer; transition: 0.2s; }
        .xhs-post:hover { transform: translateY(-5px); }
        .xhs-img { width: 100%; height: 200px; object-fit: cover; }
        .xhs-content { padding: 10px; font-size: 13px; font-weight: bold; line-height: 1.4; }

        /* ============ 4. 个人主页 ============ */
        .profile-header { background: var(--panel); padding: 20px; border-radius: 12px; margin-bottom: 20px; display: flex; gap: 20px; align-items: center;}
        .profile-avatar { width: 80px; height: 80px; border-radius: 50%; border: 3px solid var(--accent); object-fit: cover;}
        .settings-box { background: var(--panel); padding: 20px; border-radius: 12px; }
        .setting-item { display: flex; justify-content: space-between; padding: 15px 0; border-bottom: 1px solid var(--border); }

        /* 底部导航 */
        .bottom-nav { position: fixed; bottom: 0; width: 100%; height: 70px; background: var(--panel); border-top: 1px solid var(--border); display: flex; justify-content: space-around; align-items: center; z-index: 100; }
        .nav-btn { display: flex; flex-direction: column; align-items: center; font-size: 11px; color: var(--sub); cursor: pointer; transition: 0.2s; }
        .nav-btn.active { color: var(--accent); font-weight: bold;}
        .nav-icon { font-size: 22px; margin-bottom: 4px; }

        /* 弹窗 */
        .modal { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 999; display: none; justify-content: center; align-items: center; }
        .modal-content { background: var(--panel); width: 80%; max-width: 400px; padding: 30px; border-radius: 20px; text-align: center; }
    </style>
</head>
<body data-theme="light">

    <div class="top-bar">
        <div class="logo">HOMETREE.</div>
        <button class="theme-btn" onclick="toggleTheme()">🌙</button>
    </div>

    <!-- ================= 页面 1：滑动匹配 ================= -->
    <div class="page active" id="page-match">
        <div class="match-wrapper">
            <div class="card-container" id="cardContainer">
                <!-- JS 自动渲染 10 张卡片 -->
            </div>
            <div class="controls">
                <button class="btn" onclick="swipe('left')">✕</button>
                <button class="btn btn-like" onclick="swipe('right')">♥</button>
            </div>
        </div>
    </div>

    <!-- ================= 页面 2：二手书市 ================= -->
    <div class="page" id="page-market">
        <h2 style="margin-bottom:20px;">多抓鱼书市 (二手漂流)</h2>
        <div class="market-grid">
            <div class="book-item">
                <img src="https://img9.doubanio.com/view/subject/s/public/s28385152.jpg" class="book-cover">
                <div class="book-info">
                    <h3>撒哈拉的故事</h3>
                    <p style="font-size:12px;color:var(--sub);">三毛 | 9成新</p>
                    <div class="book-price">¥ 12.00</div>
                    <button class="buy-btn">加入书袋</button>
                </div>
            </div>
            <div class="book-item">
                <img src="https://img9.doubanio.com/view/subject/s/public/s27310421.jpg" class="book-cover">
                <div class="book-info">
                    <h3>我的天才女友</h3>
                    <p style="font-size:12px;color:var(--sub);">费兰特 | 8成新</p>
                    <div class="book-price">¥ 18.50</div>
                    <button class="buy-btn">加入书袋</button>
                </div>
            </div>
            <div class="book-item">
                <img src="https://img3.doubanio.com/view/subject/s/public/s33747736.jpg" class="book-cover">
                <div class="book-info">
                    <h3>正常人</h3>
                    <p style="font-size:12px;color:var(--sub);">萨莉·鲁尼 | 全新</p>
                    <div class="book-price">¥ 25.00</div>
                    <button class="buy-btn">加入书袋</button>
                </div>
            </div>
        </div>
    </div>

    <!-- ================= 页面 3：精神社区 (小红书风) ================= -->
    <div class="page" id="page-community">
        <h2 style="margin-bottom:20px;">精神自留地</h2>
        <div class="xhs-grid">
            <div class="xhs-post">
                <img src="https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=500" class="xhs-img">
                <div class="xhs-content">罗大佑的歌词，句句都是时代挽歌。<br><span style="color:var(--sub);font-weight:normal;font-size:11px;">#罗大佑 #鹿港小镇</span></div>
            </div>
            <div class="xhs-post">
                <img src="https://images.unsplash.com/photo-1520637836862-4d197d17c90a?w=500" class="xhs-img">
                <div class="xhs-content">重看《搏击俱乐部》，还是被 Tyler 震撼。<br><span style="color:var(--sub);font-weight:normal;font-size:11px;">#搏击俱乐部 #虚无主义</span></div>
            </div>
            <div class="xhs-post">
                <img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=500" class="xhs-img">
                <div class="xhs-content">Björk 的现场是一场极光祭祀。<br><span style="color:var(--sub);font-weight:normal;font-size:11px;">#Björk #实验电子</span></div>
            </div>
        </div>
    </div>

    <!-- ================= 页面 4：我的与隐私 ================= -->
    <div class="page" id="page-profile">
        <div class="profile-header">
            <img src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=200" class="profile-avatar">
            <div>
                <h2 style="margin-bottom:5px;">Yiming</h2>
                <p style="color:var(--sub); font-size:13px;">已接入：豆瓣 126本在读 | 网易云 89首</p>
            </div>
        </div>
        <h3 style="margin-bottom:10px;">隐私与设置</h3>
        <div class="settings-box">
            <div class="setting-item">
                <span>隐身模式（不被推荐）</span>
                <input type="checkbox">
            </div>
            <div class="setting-item">
                <span>屏蔽与拉黑管理</span>
                <span style="color:var(--accent); cursor:pointer;">查看 (2)</span>
            </div>
            <div class="setting-item" style="border:none;">
                <span>退出登录</span>
                <span style="color:red; cursor:pointer;">退出</span>
            </div>
        </div>
    </div>

    <!-- 底部导航栏 -->
    <div class="bottom-nav">
        <div class="nav-btn active" onclick="switchPage('page-match', this)"><span class="nav-icon">🔥</span><span>匹配</span></div>
        <div class="nav-btn" onclick="switchPage('page-market', this)"><span class="nav-icon">📚</span><span>书市</span></div>
        <div class="nav-btn" onclick="switchPage('page-community', this)"><span class="nav-icon">🌸</span><span>社区</span></div>
        <div class="nav-btn" onclick="switchPage('page-profile', this)"><span class="nav-icon">👤</span><span>我的</span></div>
    </div>

    <!-- 匹配成功弹窗 -->
    <div class="modal" id="matchModal">
        <div class="modal-content">
            <h2 style="color:var(--accent); margin-bottom:10px;">FREQUENCY ALIGNED!</h2>
            <p>你们的精神频率已对齐。</p>
            <button style="margin-top:20px; padding:10px 20px; background:var(--accent); color:white; border:none; border-radius:20px; cursor:pointer;" onclick="document.getElementById('matchModal').style.display='none'">发消息</button>
        </div>
    </div>

    <script>
        // ================= 1. 真实的 10 张卡片数据 =================
        const users = [
            { name: "娄烨", age: 58, img: "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=600", tags: ["苏州河", "推拿", "第六代导演"], quote: "如果有一天我走了，你会像马达那样找我吗？", ai: "AI: 适合在雨天聊贾宏声。" },
            { name: "Tyler Durden", age: 30, img: "https://images.unsplash.com/photo-1520637836862-4d197d17c90a?w=600", tags: ["Fight Club", "Nihilism", "反消费主义"], quote: "You are not your job. You are not your bank account.", ai: "AI: 别聊工作，聊地下搏击。" },
            { name: "Morrissey", age: 64, img: "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?w=600", tags: ["The Smiths", "Jangle Pop", "抑郁"], quote: "There is a light that never goes out.", ai: "AI: 深夜 emo 必备。请备好红酒。" },
            { name: "Björk", age: 58, img: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600", tags: ["Art Pop", "Homogenic", "冰岛"], quote: "I'm carried by the storm, I'm the spark.", ai: "AI: 冰岛极光与实验电子。匹配度 99%。" },
            { name: "罗大佑", age: 68, img: "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=600", tags: ["鹿港小镇", "时代挽歌"], quote: "台北不是我的家，我的家乡没有霓虹灯。", ai: "AI: 午夜聊华语启蒙。" },
            { name: "Emo Kid", age: 22, img: "https://images.unsplash.com/photo-1501386761578-eac5c94b800a?w=600", tags: ["Midwest Emo", "Math Rock"], quote: "Let's just be friends... or play in drop D.", ai: "AI: 沉浸在延迟效果器里的男孩。" },
            { name: "Matt Bellamy", age: 45, img: "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=600", tags: ["Muse", "Space Rock", "Falsetto"], quote: "This is the last time I'll abandon you.", ai: "AI: 极度沉迷科幻和反乌托邦。" },
            { name: "Aphex Twin", age: 52, img: "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=600", tags: ["IDM", "Ambient Techno", "DSP"], quote: "I want to make music that makes people feel weird.", ai: "AI: 问你 Windowlicker 的碎拍怎么切。" },
            { name: "Kurt Cobain", age: 27, img: "https://images.unsplash.com/photo-1520637836862-4d197d17c90a?w=600", tags: ["Nirvana", "Grunge"], quote: "I'd rather be hated for who I am.", ai: "AI: 别聊商业，聊聊地下厂牌 Sub Pop。" },
            { name: "Kevin Shields", age: 60, img: "https://images.unsplash.com/photo-1516280440502-863a346513c1?w=600", tags: ["Shoegaze", "MBV"], quote: "Loveless is not just an album, it's a wall of sound.", ai: "AI: 噪音墙之神。问他演出的吉他调音。" }
        ];

        let currentIndex = 0;
        const container = document.getElementById('cardContainer');

        // ================= 2. 渲染卡片 =================
        function renderCards() {
            container.innerHTML = '';
            // 倒序渲染，让第一个在最上面
            for (let i = users.length - 1; i >= 0; i--) {
                if (i < currentIndex) continue; // 已经滑走的
                
                const user = users[i];
                const card = document.createElement('div');
                card.className = 'swipe-card';
                
                const offset = i - currentIndex;
                // 物理堆叠视觉
                card.style.transform = `scale(${1 - offset * 0.04}) translateY(${offset * 15}px)`;
                card.style.zIndex = -offset;
                card.style.opacity = 1 - offset * 0.15;
                
                card.innerHTML = `
                    <img src="${user.img}" class="card-img">
                    <div class="card-content">
                        <div class="name-row"><div class="name">${user.name}</div><div class="age">${user.age}</div></div>
                        <div class="tags">${user.tags.map(t => `<span class="tag">${t}</span>`).join('')}</div>
                        <div class="media-links">
                            <a href="#" class="media-btn btn-douban" onclick="event.stopPropagation(); alert('打开豆瓣：${user.tags[0]}')">豆瓣</a>
                            <a href="#" class="media-btn btn-netease" onclick="event.stopPropagation(); alert('打开网易云：${user.tags[0]}')">网易云</a>
                        </div>
                        <div class="quote">"${user.quote}"</div>
                        <div class="ai-agent">${user.ai}</div>
                    </div>
                `;
                container.appendChild(card);
            }
        }

        // ================= 3. 物理滑动逻辑 =================
        function swipe(direction) {
            // 找到当前在最顶层的卡片
            const topCard = container.querySelector(`.swipe-card[style*="z-index: 0"]`);
            if (!topCard) {
                alert("已经没有更多推荐了！");
                return;
            }

            if (direction === 'right') {
                topCard.style.transform = 'translateX(150%) rotate(20deg)';
                setTimeout(() => { document.getElementById('matchModal').style.display = 'flex'; }, 300);
            } else {
                topCard.style.transform = 'translateX(-150%) rotate(-20deg)';
            }
            
            currentIndex++;
            // 等待飞出的动画结束后，重新渲染下一张
            setTimeout(renderCards, 350); 
        }

        // ================= 4. 页面切换与主题 =================
        function switchPage(pageId, btnElement) {
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
            document.getElementById(pageId).classList.add('active');
            document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
            btnElement.classList.add('active');
        }

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

components.html(html_code, height=900, scrolling=False)
