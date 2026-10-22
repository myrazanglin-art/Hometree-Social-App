import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hometree", layout="wide", initial_sidebar_state="collapsed")

html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root {
            --bg: #0B0B0C; /* 极简黑底色 */
            --card: #1A1A1C; /* 卡片微灰 */
            --text: #F2F2F7;
            --sub: #8E8E93;
            --accent: #FF69B4; /* 赛博粉 */
            --accent-glow: rgba(255, 105, 180, 0.4);
            --border: #333336;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Courier, monospace; }
        body { background: var(--bg); color: var(--text); height: 100vh; display: flex; justify-content: center; align-items: center; overflow: hidden; }
        
        /* 手机外壳 (极简工业风) */
        .app-container { width: 375px; height: 812px; background: var(--bg); border-radius: 20px; box-shadow: 0 0 50px rgba(0,0,0,0.8); overflow: hidden; position: relative; display: flex; flex-direction: column; border: 1px solid var(--border); }

        /* 登录页 */
        .login-screen { flex: 1; display: flex; flex-direction: column; justify-content: center; padding: 40px; background: var(--bg); z-index: 10; }
        .logo { font-size: 32px; font-weight: 800; color: var(--text); text-align: center; margin-bottom: 10px; letter-spacing: -1px;}
        .slogan { text-align: center; font-size: 12px; color: var(--sub); margin-bottom: 40px; font-style: italic; }
        .login-btn { width: 100%; padding: 15px; border-radius: 4px; border: 1px solid var(--border); background: transparent; color: var(--text); font-size: 14px; margin-bottom: 15px; cursor: pointer; transition: 0.3s; letter-spacing: 1px;}
        .login-btn:hover { border-color: var(--accent); color: var(--accent); }
        
        /* 主界面 */
        .main-screen { flex: 1; display: none; flex-direction: column; position: relative; }
        
        .header { padding: 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); }
        .header-title { font-weight: bold; font-size: 16px; letter-spacing: 2px; color: var(--accent); }
        
        /* 卡片区 */
        .card-deck { flex: 1; position: relative; padding: 20px; display: flex; justify-content: center; align-items: center; }
        .swipe-card { width: 100%; height: 100%; background: var(--card); border-radius: 8px; border: 1px solid var(--border); box-shadow: 0 10px 30px rgba(0,0,0,0.5); overflow: hidden; position: absolute; transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), opacity 0.4s ease; display: flex; flex-direction: column; }
        .swipe-card img { width: 100%; height: 55%; object-fit: cover; filter: grayscale(80%) contrast(120%); transition: filter 0.3s; }
        .swipe-card:hover img { filter: grayscale(20%) contrast(100%); }
        
        .card-content { padding: 20px; flex: 1; display: flex; flex-direction: column; }
        .name-row { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 12px; }
        .name { font-size: 22px; font-weight: 800; letter-spacing: -0.5px;}
        .age { color: var(--sub); font-size: 14px; font-family: monospace;}
        
        .tags { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 15px; }
        .tag { background: transparent; border: 1px solid var(--accent); color: var(--accent); padding: 3px 8px; border-radius: 2px; font-size: 11px; letter-spacing: 0.5px; }
        
        .quote { font-size: 13px; color: var(--text); line-height: 1.6; font-style: italic; margin-bottom: 15px; border-left: 1px solid var(--sub); padding-left: 10px;}
        
        .ai-bio { font-size: 12px; color: var(--accent); line-height: 1.5; font-family: monospace; margin-top: auto; padding-top: 10px; border-top: 1px dashed var(--border);}
        
        /* 操作栏 */
        .action-bar { padding: 20px; display: flex; justify-content: space-around; align-items: center; border-top: 1px solid var(--border); background: var(--bg); }
        .btn { width: 55px; height: 55px; border-radius: 50%; border: 1px solid var(--border); font-size: 20px; cursor: pointer; display: flex; justify-content: center; align-items: center; background: transparent; color: var(--text); transition: 0.2s; }
        .btn:hover { border-color: var(--accent); color: var(--accent); box-shadow: 0 0 15px var(--accent-glow); }
        .btn-like { width: 65px; height: 65px; border-color: var(--accent); color: var(--accent); font-size: 26px;}

        /* 底部 Tab */
        .tab-bar { display: flex; justify-content: space-around; padding: 15px 0; border-top: 1px solid var(--border); background: var(--bg); }
        .tab { color: var(--sub); font-size: 18px; cursor: pointer; }
        .tab.active { color: var(--accent); }

        /* 匹配弹窗 (搏击俱乐部风格) */
        .match-modal { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(11, 11, 12, 0.95); backdrop-filter: blur(5px); z-index: 100; display: none; flex-direction: column; justify-content: center; align-items: center; padding: 30px; text-align: center; }
        .match-title { font-size: 28px; font-weight: 900; color: var(--accent); margin-bottom: 10px; font-family: monospace; letter-spacing: 2px;}
        .match-sub { font-size: 14px; color: var(--sub); margin-bottom: 30px; font-style: italic;}
        .chat-btn { width: 100%; padding: 15px; border-radius: 4px; border: 1px solid var(--accent); background: transparent; color: var(--accent); font-size: 14px; font-weight: bold; cursor: pointer; transition: 0.3s;}
        .chat-btn:hover { background: var(--accent); color: var(--bg); }
    </style>
</head>
<body>

    <div class="app-container">
        
        <!-- 登录页 -->
        <div class="login-screen" id="loginScreen">
            <div class="logo">HOMETREE.</div>
            <div class="slogan">"You are not your job. You are not your bank account."</div>
            <button class="login-btn" onclick="login()">SYNC WECHAT / 微信</button>
            <button class="login-btn" onclick="alert('Fetching Douban data...')">SYNC DOUBAN / 豆瓣书影音</button>
            <button class="login-btn" onclick="alert('Fetching NetEase playlists...')">SYNC NETEASE / 网易云</button>
        </div>

        <!-- 主界面 -->
        <div class="main-screen" id="mainScreen">
            <div class="header">
                <div class="header-title">FIND YOUR FREQUENCY</div>
                <div style="color:var(--sub);">⚙</div>
            </div>
            
            <div class="card-deck" id="cardDeck">
                
                <!-- 1. 罗大佑 -->
                <div class="swipe-card" style="transform: scale(0.9) translateY(40px); z-index: -2; opacity: 0.2;">
                    <img src="https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=600&q=80">
                    <div class="card-content">
                        <div class="name-row"><div class="name">Lo Ta-Yu</div><div class="age">68</div></div>
                        <div class="tags"><span class="tag">罗大佑</span><span class="tag">鹿港小镇</span><span class="tag">时代挽歌</span></div>
                        <div class="quote">"台北不是我的家，我的家乡没有霓虹灯。"</div>
                        <div class="ai-bio">AI AGENT: 沧桑的灵魂，适合在午夜聊华语流行乐的启蒙。</div>
                    </div>
                </div>

                <!-- 2. Björk -->
                <div class="swipe-card" style="transform: scale(0.92) translateY(30px); z-index: -2; opacity: 0.3;">
                    <img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=600&q=80">
                    <div class="card-content">
                        <div class="name-row"><div class="name">Björk</div><div class="age">58</div></div>
                        <div class="tags"><span class="tag">Björk</span><span class="tag">Homogenic</span><span class="tag">Art Pop</span></div>
                        <div class="quote">"I'm carried by the storm, I'm the spark."</div>
                        <div class="ai-bio">AI AGENT: 匹配度 99%。她的声音是冰岛的极光，也是你实验电子乐的最爱。</div>
                    </div>
                </div>

                <!-- 3. Midwest Emo (American Football) -->
                <div class="swipe-card" style="transform: scale(0.94) translateY(20px); z-index: -1; opacity: 0.4;">
                    <img src="https://images.unsplash.com/photo-1501386761578-eac5c94b800a?auto=format&fit=crop&w=600&q=80">
                    <div class="card-content">
                        <div class="name-row"><div class="name">Emo Kid</div><div class="age">22</div></div>
                        <div class="tags"><span class="tag">American Football</span><span class="tag">Midwest Emo</span><span class="tag">Math Rock</span></div>
                        <div class="quote">"Let's just be friends... or play in drop D."</div>
                        <div class="ai-bio">AI AGENT: 沉浸在延迟效果器里的男孩。你们的共同话题：Never Meant。</div>
                    </div>
                </div>

                <!-- 4. The Smiths -->
                <div class="swipe-card" style="transform: scale(0.96) translateY(10px); z-index: 0; opacity: 0.6;">
                    <img src="https://images.unsplash.com/photo-1493225457124-a1a2a5f5646a?auto=format&fit=crop&w=600&q=80">
                    <div class="card-content">
                        <div class="name-row"><div class="name">Morrissey</div><div class="age">64</div></div>
                        <div class="tags"><span class="tag">The Smiths</span><span class="tag">Jangle Pop</span><span class="tag">忧郁</span></div>
                        <div class="quote">"And if a double-decker bus crashes into us..."</div>
                        <div class="ai-bio">AI AGENT: 主页那句 There Is a Light 就是为他留的。开口就对暗号。</div>
                    </div>
                </div>

                <!-- 5. 搏击俱乐部 Tyler Durden -->
                <div class="swipe-card" style="transform: scale(0.98) translateY(5px); z-index: 1; opacity: 0.8;">
                    <img src="https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&w=600&q=80">
                    <div class="card-content">
                        <div class="name-row"><div class="name">Tyler Durden</div><div class="age">30</div></div>
                        <div class="tags"><span class="tag">Fight Club</span><span class="tag">Nihilism</span><span class="tag">Soap</span></div>
                        <div class="quote">"It's only after we've lost everything that we're free to do anything."</div>
                        <div class="ai-bio">AI AGENT: 别跟他聊工作。他极度讨厌消费主义，你可以约他去地下搏击场。</div>
                    </div>
                </div>

                <!-- 6. Muse (Matt Bellamy) -->
                <div class="swipe-card" style="transform: scale(1) translateY(0px); z-index: 2; opacity: 0.9;">
                    <img src="https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?auto=format&fit=crop&w=600&q=80">
                    <div class="card-content">
                        <div class="name-row"><div class="name">Matt Bellamy</div><div class="age">45</div></div>
                        <div class="tags"><span class="tag">Muse</span><span class="tag">Space Rock</span><span class="tag">Falsetto</span></div>
                        <div class="quote">"This is the last time I'll abandon you."</div>
                        <div class="ai-bio">AI AGENT: 警告：此人极度沉迷科幻和反乌托邦。问他关于 Plug in Baby 的吉他 Riff。</div>
                    </div>
                </div>

                <!-- 7. 实验电子 (Aphex Twin) -->
                <div class="swipe-card" style="transform: scale(1) translateY(0px); z-index: 3; opacity: 1;">
                    <img src="https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=600&q=80">
                    <div class="card-content">
                        <div class="name-row"><div class="name">Aphex Twin</div><div class="age">52</div></div>
                        <div class="tags"><span class="tag">IDM</span><span class="tag">Ambient Techno</span><span class="tag">DSP</span></div>
                        <div class="quote">"I want to make music that makes people feel weird."</div>
                        <div class="ai-bio">AI AGENT: 你们都在玩 Max/MSP。问他 Windowlicker 里的碎拍是怎么切出来的。</div>
                    </div>
                </div>

                <!-- 8. 小众电影 (王家卫) -->
                <div class="swipe-card" style="transform: scale(1) translateY(0px); z-index: 4; opacity: 1;">
                    <img src="https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&w=600&q=80">
                    <div class="card-content">
                        <div class="name-row"><div class="name">Wong Kar-wai</div><div class="age">65</div></div>
                        <div class="tags"><span class="tag">王家卫</span><span class="tag">重庆森林</span><span class="tag">杜可风</span></div>
                        <div class="quote">"不知道从什么时候开始，在什么东西上面都有个日期。"</div>
                        <div class="ai-bio">AI AGENT: 视觉与情绪的顶级大师。聊聊《堕落天使》里的广角镜头。</div>
                    </div>
                </div>

                <!-- 9. Shoegaze (My Bloody Valentine) -->
                <div class="swipe-card" style="transform: scale(1) translateY(0px); z-index: 5; opacity: 1;">
                    <img src="https://images.unsplash.com/photo-1516280440502-863a346513c1?auto=format&fit=crop&w=600&q=80">
                    <div class="card-content">
                        <div class="name-row"><div class="name">Kevin Shields</div><div class="age">60</div></div>
                        <div class="tags"><span class="tag">Shoegaze</span><span class="tag">MBV</span><span class="tag">Glide Guitar</span></div>
                        <div class="quote">"Loveless is not just an album, it's a wall of sound."</div>
                        <div class="ai-bio">AI AGENT: 沉浸在噪音墙里的神。你问他演出时吉他到底调了什么音。</div>
                    </div>
                </div>

                <!-- 10. 摇滚/朋克 (Kurt Cobain) -->
                <div class="swipe-card" style="transform: scale(1) translateY(0px); z-index: 6; opacity: 1;">
                    <img src="https://images.unsplash.com/photo-1520637836862-4d197d17c90a?auto=format&fit=crop&w=600&q=80">
                    <div class="card-content">
                        <div class="name-row"><div class="name">Kurt Cobain</div><div class="age">27</div></div>
                        <div class="tags"><span class="tag">Nirvana</span><span class="tag">Grunge</span><span class="tag">Olympia</span></div>
                        <div class="quote">"I'd rather be hated for who I am, than loved for who I am not."</div>
                        <div class="ai-bio">AI AGENT: 吉他噪音、撕裂的嗓音。别聊商业，聊聊地下厂牌（Sub Pop）。</div>
                    </div>
                </div>

            </div>

            <!-- 操作按钮 -->
            <div class="action-bar">
                <button class="btn" onclick="swipe('left')">✕</button>
                <button class="btn btn-like" onclick="swipe('right')">♥</button>
            </div>

            <!-- 底部 Tab -->
            <div class="tab-bar">
                <div class="tab active">DISCOVER</div>
                <div class="tab">CHAT</div>
                <div class="tab">PROFILE</div>
            </div>
        </div>

        <!-- Match 弹窗 -->
        <div class="match-modal" id="matchModal">
            <div class="match-title">FREQUENCY ALIGNED.</div>
            <div class="match-sub">"This is your life, and it's ending one minute at a time."</div>
            <button class="chat-btn" onclick="closeMatch()">SEND A MESSAGE</button>
        </div>

    </div>

    <script>
        let currentIndex = 0;
        const cards = document.querySelectorAll('.swipe-card');
        // 因为我们用 flex 和 z-index 堆叠了，先找出当前最上面的卡片
        let topCardZ = 6; 

        function login() {
            document.getElementById('loginScreen').style.display = 'none';
            document.getElementById('mainScreen').style.display = 'flex';
        }

        function swipe(direction) {
            const activeCard = document.querySelector(`.swipe-card[style*="z-index: ${topCardZ}"]`);
            if (!activeCard) return;

            if (direction === 'right') {
                activeCard.style.transform = 'translateX(150%) rotate(15deg)';
                setTimeout(() => {
                    activeCard.style.display = 'none';
                    showMatch();
                }, 400);
            } else {
                activeCard.style.transform = 'translateX(-150%) rotate(-15deg)';
                setTimeout(() => {
                    activeCard.style.display = 'none';
                }, 400);
            }
            
            topCardZ--;
            if(topCardZ < 0) {
                document.getElementById('cardDeck').innerHTML = '<h3 style="color:#8E8E93;font-family:monospace;">NO MORE FREQUENCIES FOUND.</h3>';
            }
        }

        function showMatch() {
            document.getElementById('matchModal').style.display = 'flex';
        }

        function closeMatch() {
            document.getElementById('matchModal').style.display = 'none';
        }
    </script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=False)
