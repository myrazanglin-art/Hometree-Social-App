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
            --bg: #121212;
            --panel: #1E1E1E;
            --text: #E0E0E0;
            --sub: #888;
            --accent: #FF69B4; 
            --border: #333;
            --qq-blue: #12B7F5;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: "Courier New", Courier, monospace; }
        body { background: var(--bg); color: var(--text); height: 100vh; display: flex; justify-content: center; align-items: center; overflow: hidden; }
        
        /* 仿古早桌面端的容器 */
        .app-container { width: 1000px; height: 750px; background: var(--panel); border-radius: 8px; box-shadow: 0 0 50px rgba(0,0,0,0.9); overflow: hidden; position: relative; display: flex; flex-direction: column; border: 1px solid var(--border); }

        /* 登录页 (极简深色) */
        .login-screen { flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; background: #0A0A0A; }
        .login-box { width: 350px; background: var(--panel); padding: 40px; border-radius: 8px; border: 1px solid var(--border); }
        .logo { font-size: 28px; font-weight: 900; color: var(--text); text-align: center; margin-bottom: 20px; letter-spacing: -1px;}
        .input-group { margin-bottom: 15px; }
        .input-group input { width: 100%; padding: 12px; background: #111; border: 1px solid var(--border); color: var(--text); border-radius: 4px; outline: none; font-family: monospace;}
        .input-group input:focus { border-color: var(--accent); }
        .login-btn { width: 100%; padding: 12px; background: var(--accent); color: #000; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; margin-bottom: 15px;}
        .oauth-row { display: flex; gap: 10px; }
        .oauth-btn { flex: 1; padding: 10px; background: transparent; border: 1px solid var(--border); color: var(--sub); border-radius: 4px; cursor: pointer; font-size: 12px;}
        .oauth-btn:hover { color: var(--text); border-color: var(--text); }

        /* 主界面 (高密度三栏布局) */
        .main-screen { flex: 1; display: none; flex-direction: column; height: 100%; }
        
        /* 顶部导航 */
        .top-bar { height: 40px; background: #111; border-bottom: 1px solid var(--border); display: flex; align-items: center; padding: 0 15px; justify-content: space-between; font-size: 12px; color: var(--sub); }
        .top-bar span { color: var(--accent); font-weight: bold;}
        
        .content-area { display: flex; flex: 1; overflow: hidden; }
        
        /* 左侧栏 (个人信息 / 栏目) */
        .sidebar { width: 220px; border-right: 1px solid var(--border); display: flex; flex-direction: column; padding: 15px; background: #151515; }
        .user-profile { display: flex; align-items: center; gap: 10px; margin-bottom: 20px; }
        .user-profile img { width: 40px; height: 40px; border-radius: 50%; border: 2px solid var(--accent); object-fit: cover;}
        .user-info h4 { font-size: 14px; color: var(--text); }
        .user-info p { font-size: 11px; color: var(--sub); }
        .nav-item { padding: 10px; font-size: 13px; color: var(--sub); cursor: pointer; border-bottom: 1px dashed #333; display: flex; justify-content: space-between;}
        .nav-item:hover { color: var(--accent); }

        /* 中间栏 (滑动卡片 - 核心) */
        .card-section { flex: 1; padding: 20px; display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; background: url('https://www.transparenttextures.com/patterns/stardust.png'); /* 加一点纹理不那么空 */ }
        
        .swipe-card { width: 100%; max-width: 480px; height: 500px; background: #000; border-radius: 8px; border: 1px solid var(--border); overflow: hidden; position: absolute; display: flex; flex-direction: column; box-shadow: 0 20px 40px rgba(0,0,0,0.6); transition: transform 0.4s ease; }
        .card-header { display: flex; align-items: center; padding: 15px; background: linear-gradient(to bottom, rgba(0,0,0,0.8), transparent); z-index: 10; position: absolute; top: 0; left: 0; right: 0; }
        .card-header img { width: 50px; height: 50px; border-radius: 4px; border: 1px solid var(--accent); margin-right: 15px; }
        .card-header .name { font-size: 20px; font-weight: bold; color: #fff; }
        .card-body-img { width: 100%; height: 300px; object-fit: cover; filter: grayscale(40%) contrast(120%); }
        .card-info { padding: 20px; flex: 1; background: #0A0A0A; display: flex; flex-direction: column; }
        .tags { display: flex; gap: 5px; flex-wrap: wrap; margin-bottom: 15px; }
        .tag { background: #222; color: var(--accent); font-size: 11px; padding: 4px 8px; border-radius: 2px; border: 1px solid #444; }
        .quote { font-size: 13px; font-style: italic; color: #CCC; margin-bottom: 15px; border-left: 2px solid var(--accent); padding-left: 10px;}
        .ai-bio { font-size: 12px; color: var(--qq-blue); font-family: monospace; margin-top: auto;}
        
        /* 操作栏 */
        .action-bar { display: flex; justify-content: center; gap: 20px; margin-top: 20px; }
        .btn { width: 60px; height: 60px; border-radius: 50%; border: 2px solid var(--border); background: #111; color: var(--text); font-size: 24px; cursor: pointer; display: flex; justify-content: center; align-items: center; transition: 0.2s;}
        .btn:hover { transform: scale(1.1); }
        .btn-like { border-color: var(--accent); color: var(--accent); }

        /* 右侧栏 (类似 QQ 空间动态，塞满内容) */
        .right-panel { width: 280px; border-left: 1px solid var(--border); padding: 15px; background: #151515; overflow-y: auto; }
        .right-title { font-size: 13px; color: var(--text); font-weight: bold; margin-bottom: 15px; border-bottom: 1px solid #333; padding-bottom: 5px;}
        .feed-item { margin-bottom: 15px; font-size: 12px; color: var(--sub); border-left: 1px solid #333; padding-left: 10px; }
        .feed-item span { color: var(--accent); }

        /* 悬浮装饰 (极繁主义) */
        .floating-decor { position: absolute; font-size: 12px; color: #555; opacity: 0.5; pointer-events: none;}

    </style>
</head>
<body>

    <div class="app-container">
        
        <!-- 登录页 -->
        <div class="login-screen" id="loginScreen">
            <div class="login-box">
                <div class="logo">HOMETREE.</div>
                <div class="input-group">
                    <input type="text" placeholder="ID / 用户名">
                </div>
                <div class="input-group">
                    <input type="password" placeholder="密码">
                </div>
                <button class="login-btn" onclick="login()">登录</button>
                <div class="oauth-row">
                    <button class="oauth-btn" onclick="alert('微信 OAuth 模拟授权...')">微信登入</button>
                    <button class="oauth-btn" onclick="alert('豆瓣 API 拉取...')">豆瓣</button>
                    <button class="oauth-btn" onclick="alert('网易云 token 获取...')">网易云</button>
                </div>
            </div>
        </div>

        <!-- 主界面 -->
        <div class="main-screen" id="mainScreen">
            <!-- 顶部状态栏 -->
            <div class="top-bar">
                <div>当前在线：<span>1,024</span> 个孤独的灵魂</div>
                <div>Current Time: 2024-10-24 23:59:59 | Connection: Secure</div>
            </div>

            <div class="content-area">
                <!-- 左侧栏 -->
                <div class="sidebar">
                    <div class="user-profile">
                        <img src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=100&q=80">
                        <div class="user-info">
                            <h4>Yiming</h4>
                            <p>情绪稳定 / 亚文化</p>
                        </div>
                    </div>
                    <div class="nav-item"><span>📁 我的书影音</span> <span>24</span></div>
                    <div class="nav-item"><span>💬 匹配消息</span> <span style="color:var(--accent);">3</span></div>
                    <div class="nav-item"><span>⚙ 隐私与设置</span></div>
                    
                    <div style="margin-top:20px; font-size:11px; color:#555;">
                        // 系统日志<br/>
                        > 正在寻找频率...<br/>
                        > 剔除商业流行乐...<br/>
                        > 剔除伪文青...<br/>
                        > 匹配完成。
                    </div>
                </div>

                <!-- 中间卡片区 -->
                <div class="card-section">
                    <div class="swipe-card" style="transform: scale(0.95) translateY(20px); z-index: 1; opacity: 0.3;">
                         <div class="card-header"><img src="https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=100"><div class="name">罗大佑</div></div>
                         <img class="card-body-img" src="https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=600">
                         <div class="card-info"><div class="tags"><span class="tag">鹿港小镇</span><span class="tag">时代挽歌</span></div></div>
                    </div>
                    <div class="swipe-card" style="transform: scale(0.97) translateY(10px); z-index: 2; opacity: 0.5;">
                         <div class="card-header"><img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=100"><div class="name">Björk</div></div>
                         <img class="card-body-img" src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600">
                         <div class="card-info"><div class="tags"><span class="tag">Homogenic</span><span class="tag">Art Pop</span></div></div>
                    </div>
                    <div class="swipe-card" style="transform: scale(0.99) translateY(5px); z-index: 3; opacity: 0.7;">
                         <div class="card-header"><img src="https://images.unsplash.com/photo-1501386761578-eac5c94b800a?w=100"><div class="name">Midwest Emo</div></div>
                         <img class="card-body-img" src="https://images.unsplash.com/photo-1501386761578-eac5c94b800a?w=600">
                         <div class="card-info"><div class="tags"><span class="tag">American Football</span><span class="tag">Math Rock</span></div></div>
                    </div>
                    
                    <!-- 娄烨 -->
                    <div class="swipe-card" style="transform: scale(1) translateY(0px); z-index: 4; opacity: 0.9;">
                         <div class="card-header"><img src="https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=100"><div class="name">娄烨</div></div>
                         <img class="card-body-img" src="https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=600">
                         <div class="card-info">
                             <div class="tags"><span class="tag">苏州河</span><span class="tag">推拿</span><span class="tag">摇晃镜头</span></div>
                             <div class="quote">"如果有一天我走了，你会像马达那样找我吗？"</div>
                             <div class="ai-bio">AI AGENT: 潮湿、阴郁、手持摄影。适合在下雨的下午聊聊贾宏声。</div>
                         </div>
                    </div>

                    <!-- 搏击俱乐部 Tyler Durden -->
                    <div class="swipe-card" style="transform: scale(1) translateY(0px); z-index: 5; opacity: 1;">
                         <div class="card-header"><img src="https://images.unsplash.com/photo-1520637836862-4d197d17c90a?w=100"><div class="name">Tyler Durden</div></div>
                         <img class="card-body-img" src="https://images.unsplash.com/photo-1520637836862-4d197d17c90a?w=600">
                         <div class="card-info">
                             <div class="tags"><span class="tag">Fight Club</span><span class="tag">Nihilism</span><span class="tag">Soap</span></div>
                             <div class="quote">"It's only after we've lost everything that we're free to do anything."</div>
                             <div class="ai-bio">AI AGENT: 警惕消费主义陷阱。建议直接约他去地下室打一架。</div>
                         </div>
                    </div>

                    <!-- 更多卡片... -->
                     <div class="swipe-card" style="transform: scale(1) translateY(0px); z-index: 6; opacity: 1;">
                         <div class="card-header"><img src="https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?w=100"><div class="name">The Smiths</div></div>
                         <img class="card-body-img" src="https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?w=600">
                         <div class="card-info">
                             <div class="tags"><span class="tag">Morrissey</span><span class="tag">Jangle Pop</span><span class="tag">抑郁</span></div>
                             <div class="quote">"And if a double-decker bus crashes into us..."</div>
                             <div class="ai-bio">AI AGENT: 深夜 emo 专属。请备好红酒和抗抑郁药。</div>
                         </div>
                    </div>
                    
                    <div class="action-bar">
                        <button class="btn" onclick="swipeCard('left')">✕</button>
                        <button class="btn btn-like" onclick="swipeCard('right')">♥</button>
                    </div>
                </div>

                <!-- 右侧栏 -->
                <div class="right-panel">
                    <div class="right-title">RECENT FREQUENCIES / 最近同频</div>
                    <div class="feed-item"><span>Yuki</span> 刚刚收藏了 《The Queen Is Dead》</div>
                    <div class="feed-item"><span>Tyler</span> 在 Fight Club 留下了新伤疤</div>
                    <div class="feed-item"><span>娄烨</span> 正在循环 《一场游戏一场梦》</div>
                    <div class="feed-item"><span>Björk</span> 上传了新照片 (冰岛极光)</div>
                    <div class="feed-item"><span>Emo Kid</span> 修改了个签: I'm just a kid and life is a nightmare.</div>
                    <div class="feed-item"><span>Aphex Twin</span> 在线 (挂机中)</div>
                    <div class="feed-item"><span>罗大佑</span> 退出了群聊</div>
                    <div class="feed-item"><span>Kurt</span> 正在听 Smells Like Teen Spirit</div>
                    
                    <div class="right-title" style="margin-top: 30px;">SYSTEM MESSAGES</div>
                    <div class="feed-item" style="border:none; color:#555;">> 系统已为您过滤 99% 的庸俗用户。</div>
                    <div class="feed-item" style="border:none; color:#555;">> Hometree v0.1.0-beta</div>
                </div>
            </div>
            
            <!-- 装饰性文字 -->
            <div class="floating-decor" style="bottom: 20px; left: 250px;">*User authentication simulated. DB not connected.*</div>
        </div>

    </div>

    <script>
        let currentZ = 6;

        function login() {
            document.getElementById('loginScreen').style.display = 'none';
            document.getElementById('mainScreen').style.display = 'flex';
        }

        function swipeCard(direction) {
            // 找到当前最顶部的卡片
            const activeCard = document.querySelector(`.swipe-card[style*="z-index: ${currentZ}"]`);
            if (!activeCard) return;

            if (direction === 'right') {
                activeCard.style.transform = 'translateX(150%) rotate(15deg)';
                setTimeout(() => {
                    activeCard.style.display = 'none';
                    alert("MATCHED. 信号已连接。");
                }, 400);
            } else {
                activeCard.style.transform = 'translateX(-150%) rotate(-15deg)';
                setTimeout(() => {
                    activeCard.style.display = 'none';
                }, 400);
            }
            
            // 弹出最上面的卡片后，把下一张卡片的透明度调高
            currentZ--;
            if(currentZ > 0) {
                 const nextCard = document.querySelector(`.swipe-card[style*="z-index: ${currentZ}"]`);
                 if(nextCard) {
                     nextCard.style.opacity = '1';
                     nextCard.style.transform = 'scale(1) translateY(0px)';
                 }
            }
        }
    </script>
</body>
</html>
"""

components.html(html_code, height=850, scrolling=False)
