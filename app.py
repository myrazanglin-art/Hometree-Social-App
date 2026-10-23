import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hometree", layout="wide", initial_sidebar_state="collapsed")
st.markdown(
    """
    <style>
        #MainMenu, header, footer { visibility: hidden; }
        .block-container { padding: 0 !important; max-width: 100% !important; }
        iframe { width: 100%; height: 100vh !important; height: 100dvh !important; border: 0; display: block; }
    </style>
    """,
    unsafe_allow_html=True,
)

html_code = r"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <meta name="theme-color" content="#f5f5f7">
    <style>
        :root {
            color-scheme: light;
            --bg: #f5f5f7;
            --surface: rgba(255, 255, 255, .72);
            --surface-solid: #fff;
            --text: #1d1d1f;
            --muted: #86868b;
            --line: rgba(60, 60, 67, .12);
            --accent: #e85d8e;
            --accent-soft: rgba(232, 93, 142, .12);
            --shadow: 0 18px 55px rgba(30, 30, 45, .09);
            --blur: 22px;
            --green: #16834b;
            --red: #d54747;
        }
        [data-theme="dark"] {
            color-scheme: dark;
            --bg: #101013;
            --surface: rgba(36, 36, 42, .76);
            --surface-solid: #24242a;
            --text: #f5f5f7;
            --muted: #a1a1a6;
            --line: rgba(255, 255, 255, .1);
            --accent: #ff78a9;
            --accent-soft: rgba(255, 120, 169, .14);
            --shadow: 0 18px 55px rgba(0, 0, 0, .3);
            --green: #53c98b;
            --red: #ff6961;
        }
        * { box-sizing: border-box; }
        html, body { width: 100%; height: 100%; margin: 0; }
        body {
            overflow: hidden;
            color: var(--text);
            background:
                radial-gradient(ellipse at 15% -15%, rgba(255, 190, 211, .27), transparent 34%),
                radial-gradient(ellipse at 95% 35%, rgba(187, 203, 255, .18), transparent 32%),
                var(--bg);
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", sans-serif;
            -webkit-font-smoothing: antialiased;
            transition: background .25s, color .25s;
        }
        button, input { font: inherit; }
        button { color: inherit; }
        .app { display: flex; flex-direction: column; height: 100vh; height: 100dvh; min-height: 480px; }
        .top-bar, .bottom-nav, .glass {
            background: var(--surface);
            -webkit-backdrop-filter: blur(var(--blur)) saturate(170%);
            backdrop-filter: blur(var(--blur)) saturate(170%);
        }
        .top-bar {
            height: 66px; flex: 0 0 66px; display: flex; align-items: center;
            justify-content: space-between; padding: 0 max(28px, env(safe-area-inset-left));
            border-bottom: 1px solid var(--line); z-index: 5;
        }
        .logo { font-size: 19px; font-weight: 750; letter-spacing: -.7px; }
        .logo-mark { color: var(--accent); }
        .theme-btn {
            display: inline-flex; align-items: center; gap: 8px; border: 1px solid var(--line);
            background: var(--surface); border-radius: 999px; padding: 9px 14px; cursor: pointer;
            font-size: 12px; transition: transform .2s, background .2s;
        }
        .theme-btn:hover { transform: translateY(-1px); background: var(--surface-solid); }
        .content { flex: 1; min-height: 0; position: relative; }
        .tab-page { display: none; height: 100%; overflow: auto; padding: 24px; scrollbar-width: thin; }
        .tab-page.active { display: block; animation: appear .24s ease-out; }
        @keyframes appear { from { opacity: .5; transform: translateY(4px); } to { opacity: 1; transform: none; } }
        .page-inner { max-width: 1100px; margin: 0 auto; }
        .page-heading { margin: 0 0 18px; font-size: 23px; letter-spacing: -.6px; }
        .page-subheading { color: var(--muted); font-size: 13px; margin: -10px 0 22px; }

        .match-layout { display: flex; align-items: stretch; gap: 26px; height: 100%; max-width: 1050px; margin: auto; }
        .deck-area { flex: 1; min-width: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        .card-container { width: min(100%, 360px); height: min(66vh, 560px); height: min(66dvh, 560px); min-height: 390px; position: relative; }
        .swipe-card {
            position: absolute; inset: 0; overflow: hidden; display: flex; flex-direction: column;
            border: 1px solid var(--line); border-radius: 27px; background: var(--surface-solid);
            box-shadow: var(--shadow); transform-origin: 50% 90%;
            transition: transform .38s cubic-bezier(.2,.8,.2,1), opacity .25s;
            touch-action: pan-y; user-select: none;
        }
        .card-img { display: block; width: 100%; height: 48%; min-height: 170px; object-fit: cover; background: var(--bg); }
        .card-info { min-height: 0; flex: 1; display: flex; flex-direction: column; padding: 17px 19px 18px; }
        .name-row { display: flex; align-items: baseline; gap: 9px; margin-bottom: 9px; }
        .name { font-size: 22px; font-weight: 720; letter-spacing: -.5px; }
        .age { color: var(--muted); font-size: 13px; }
        .tags, .media-links { display: flex; flex-wrap: wrap; gap: 7px; margin-bottom: 11px; }
        .tag { border-radius: 999px; padding: 5px 10px; background: var(--accent-soft); color: var(--accent); font-size: 11px; }
        .media-btn { border: 1px solid var(--line); border-radius: 999px; padding: 5px 10px; font-size: 10px; cursor: pointer; }
        .btn-douban { color: var(--green); }
        .btn-netease { color: var(--red); }
        .quote { flex: 1; min-height: 24px; color: var(--muted); font-size: 13px; line-height: 1.5; font-style: italic; }
        .ai-agent { display: inline-flex; align-self: flex-start; padding: 8px 10px; border-radius: 11px; background: var(--bg); color: var(--muted); font-size: 11px; }
        .controls { display: flex; align-items: center; justify-content: center; gap: 19px; padding-top: 17px; }
        .btn {
            width: 52px; height: 52px; display: grid; place-items: center; border-radius: 50%;
            border: 1px solid var(--line); background: var(--surface); box-shadow: 0 5px 18px rgba(0,0,0,.07);
            cursor: pointer; font-size: 19px; transition: transform .18s, box-shadow .18s, background .18s;
        }
        .btn:hover { transform: translateY(-3px); box-shadow: 0 9px 22px rgba(0,0,0,.12); }
        .btn:active { transform: scale(.94); }
        .btn-like { width: 60px; height: 60px; color: var(--accent); font-size: 24px; border-color: var(--accent); background: var(--accent-soft); }
        .matches-sidebar { width: 290px; flex: 0 0 290px; align-self: center; max-height: 78%; overflow: auto; padding: 18px; border: 1px solid var(--line); border-radius: 22px; box-shadow: var(--shadow); }
        .matches-title { padding-bottom: 13px; border-bottom: 1px solid var(--line); font-size: 14px; font-weight: 700; }
        .match-item { display: flex; align-items: center; gap: 11px; padding: 11px 8px; margin: 3px -8px; border-radius: 13px; cursor: pointer; transition: background .18s; }
        .match-item:hover { background: var(--accent-soft); }
        .match-avatar { width: 43px; height: 43px; flex: 0 0 43px; object-fit: cover; border-radius: 50%; }
        .match-info { flex: 1; min-width: 0; }
        .match-name { font-size: 13px; font-weight: 650; }
        .match-last { overflow: hidden; white-space: nowrap; text-overflow: ellipsis; color: var(--muted); font-size: 11px; margin-top: 4px; }
        .empty-matches { padding: 24px 8px 10px; color: var(--muted); font-size: 12px; text-align: center; }

        .market-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 300px), 1fr)); gap: 15px; }
        .book-item { display: flex; gap: 15px; padding: 14px; border: 1px solid var(--line); border-radius: 18px; background: var(--surface); -webkit-backdrop-filter: blur(var(--blur)); backdrop-filter: blur(var(--blur)); transition: transform .2s, box-shadow .2s; }
        .book-item:hover { transform: translateY(-3px); box-shadow: var(--shadow); }
        .book-cover { width: 75px; height: 108px; object-fit: cover; border-radius: 8px; background: var(--bg); }
        .book-info { flex: 1; min-width: 0; display: flex; flex-direction: column; }
        .book-title { font-size: 14px; font-weight: 700; margin: 3px 0 6px; }
        .book-meta { color: var(--muted); font-size: 11px; }
        .book-price { display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-top: auto; color: var(--accent); font-size: 14px; font-weight: 700; }
        .buy-btn { border: 0; border-radius: 999px; padding: 8px 11px; color: #fff; background: var(--accent); font-size: 11px; cursor: pointer; }
        .buy-btn:active { transform: scale(.96); }

        .xhs-masonry { columns: 3 220px; column-gap: 16px; }
        .xhs-card { overflow: hidden; break-inside: avoid; margin: 0 0 16px; border: 1px solid var(--line); border-radius: 18px; background: var(--surface); box-shadow: 0 8px 24px rgba(20,20,30,.04); }
        .xhs-img { display: block; width: 100%; object-fit: cover; }
        .xhs-content { padding: 12px 13px 9px; font-size: 13px; font-weight: 650; line-height: 1.5; }
        .xhs-author { display: flex; align-items: center; gap: 8px; padding: 0 13px 13px; color: var(--muted); font-size: 11px; }
        .xhs-avatar { width: 23px; height: 23px; border-radius: 50%; object-fit: cover; }

        .profile-header { display: flex; align-items: center; gap: 17px; padding: 20px; margin-bottom: 18px; border: 1px solid var(--line); border-radius: 20px; background: var(--surface); }
        .avatar { width: 68px; height: 68px; object-fit: cover; border-radius: 20px; }
        .profile-header h2 { margin: 0; font-size: 19px; }
        .profile-header p { margin: 6px 0 0; color: var(--muted); font-size: 12px; }
        .settings-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
        .setting-card { display: flex; justify-content: space-between; align-items: center; gap: 10px; min-height: 58px; padding: 14px 16px; border: 1px solid var(--line); border-radius: 15px; background: var(--surface); font-size: 13px; }
        .setting-action { color: var(--accent); cursor: pointer; white-space: nowrap; }
        .toggle { width: 42px; height: 25px; flex: 0 0 42px; position: relative; border-radius: 999px; background: var(--line); cursor: pointer; transition: background .2s; }
        .toggle::after { content: ""; position: absolute; top: 3px; left: 3px; width: 19px; height: 19px; border-radius: 50%; background: white; box-shadow: 0 1px 4px #0002; transition: transform .2s; }
        .toggle.active { background: #34c759; }
        .toggle.active::after { transform: translateX(17px); }

        .bottom-nav { height: 72px; flex: 0 0 72px; display: flex; justify-content: center; gap: min(8vw, 90px); align-items: center; border-top: 1px solid var(--line); padding-bottom: env(safe-area-inset-bottom); z-index: 5; }
        .nav-item { min-width: 58px; display: flex; flex-direction: column; align-items: center; gap: 3px; color: var(--muted); cursor: pointer; font-size: 10px; transition: color .2s, transform .2s; }
        .nav-item:hover { transform: translateY(-2px); }
        .nav-item.active { color: var(--accent); }
        .nav-icon { font-size: 19px; line-height: 1; }

        .chat-modal { position: fixed; inset: 0; z-index: 20; display: none; flex-direction: column; background: var(--bg); }
        .chat-header { display: flex; align-items: center; gap: 12px; min-height: 66px; padding: 10px 18px; border-bottom: 1px solid var(--line); background: var(--surface); -webkit-backdrop-filter: blur(var(--blur)); backdrop-filter: blur(var(--blur)); }
        .back-btn { width: 38px; height: 38px; border: 0; border-radius: 50%; background: var(--accent-soft); color: var(--accent); font-size: 20px; cursor: pointer; }
        .chat-avatar { width: 38px; height: 38px; border-radius: 50%; object-fit: cover; }
        .chat-name { font-size: 15px; font-weight: 700; }
        .chat-body { flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; padding: 22px max(18px, calc((100% - 720px)/2)); }
        .msg { max-width: min(78%, 520px); padding: 11px 15px; border-radius: 19px; font-size: 14px; line-height: 1.5; overflow-wrap: anywhere; }
        .msg-left { align-self: flex-start; border: 1px solid var(--line); border-bottom-left-radius: 6px; background: var(--surface-solid); }
        .msg-right { align-self: flex-end; border-bottom-right-radius: 6px; background: var(--accent); color: #fff; }
        .chat-input-area { display: flex; gap: 9px; padding: 12px max(16px, calc((100% - 720px)/2)); padding-bottom: max(12px, env(safe-area-inset-bottom)); border-top: 1px solid var(--line); background: var(--surface); }
        .chat-input { min-width: 0; flex: 1; padding: 12px 15px; border: 1px solid var(--line); border-radius: 999px; outline: 0; color: var(--text); background: var(--bg); }
        .chat-input:focus { border-color: var(--accent); }
        .send-btn { border: 0; border-radius: 999px; padding: 0 19px; background: var(--accent); color: #fff; font-weight: 650; cursor: pointer; }
        button:focus-visible, .nav-item:focus-visible, .match-item:focus-visible { outline: 3px solid color-mix(in srgb, var(--accent), transparent 45%); outline-offset: 3px; }
        @media (max-width: 700px) {
            .app { min-height: 430px; }
            .top-bar { height: 56px; flex-basis: 56px; padding: 0 16px; }
            .logo { font-size: 17px; }
            .theme-btn { padding: 8px 11px; font-size: 11px; }
            .tab-page { padding: 16px; }
            .match-layout { flex-direction: column; gap: 12px; justify-content: center; }
            .deck-area { flex: 1 1 auto; min-height: 0; justify-content: center; }
            .card-container { width: min(100%, 370px); height: min(56dvh, 500px); min-height: 310px; }
            .card-img { height: 44%; min-height: 120px; }
            .card-info { padding: 13px 15px; }
            .name { font-size: 19px; }
            .controls { padding-top: 10px; gap: 15px; }
            .btn { width: 46px; height: 46px; }
            .btn-like { width: 54px; height: 54px; }
            .matches-sidebar { width: 100%; flex: 0 0 auto; align-self: stretch; max-height: 108px; padding: 9px 12px; border-radius: 16px; }
            .matches-title { padding: 0 2px 6px; border: 0; font-size: 12px; }
            #matchesList { display: flex; gap: 4px; overflow: auto; }
            .match-item { flex: 0 0 auto; padding: 5px; margin: 0; }
            .match-avatar { width: 37px; height: 37px; flex-basis: 37px; }
            .match-info { max-width: 86px; }
            .match-name { font-size: 11px; }
            .match-last { font-size: 10px; }
            .empty-matches { padding: 8px 4px; white-space: nowrap; }
            .bottom-nav { height: 64px; flex-basis: 64px; justify-content: space-around; gap: 0; }
            .nav-item { min-width: 50px; }
            .settings-grid { grid-template-columns: 1fr; }
            .page-heading { font-size: 20px; }
            .xhs-masonry { columns: 2 145px; column-gap: 10px; }
            .xhs-card { margin-bottom: 10px; border-radius: 14px; }
            .xhs-content { font-size: 12px; padding: 10px 10px 7px; }
            .xhs-author { padding: 0 10px 10px; }
            .book-item { padding: 11px; }
        }
        @media (max-height: 700px) and (min-width: 701px) {
            .card-container { height: min(58vh, 470px); min-height: 350px; }
            .matches-sidebar { max-height: 88%; }
        }
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after { scroll-behavior: auto !important; animation-duration: .01ms !important; transition-duration: .01ms !important; }
        }
    </style>
</head>
<body data-theme="light">
    <div class="app">
        <header class="top-bar">
            <div class="logo">HOMETREE<span class="logo-mark">.</span></div>
            <button class="theme-btn" id="themeButton" onclick="toggleTheme()" aria-label="switch mode"><span id="themeIcon">☾</span><span id="themeLabel">dark mode</span></button>
        </header>
        <main class="content">
            <section class="tab-page active" id="page-match">
                <div class="match-layout">
                    <div class="deck-area">
                        <div class="card-container" id="cardContainer"></div>
                        <div class="controls">
                            <button class="btn" aria-label="跳过" onclick="swipe('left')">×</button>
                            <button class="btn btn-like" aria-label="喜欢" onclick="swipe('right')">♥</button>
                        </div>
                    </div>
                    <aside class="matches-sidebar glass">
                        <div class="matches-title">消息匹配 <span id="matchesCount"></span></div>
                        <div id="matchesList"></div>
                    </aside>
                </div>
            </section>
            <section class="tab-page" id="page-market">
                <div class="page-inner">
                    <h1 class="page-heading">书市</h1><p class="page-subheading">让喜欢的书，继续流动。</p>
                    <div class="market-grid">
                        <!-- 撒哈拉 -->
                        <article class="book-item"><img src="https://raw.githubusercontent.com/myrazanglin-art/Hometree-Social-App/main/images/撒哈拉.jpg" class="book-cover" alt="撒哈拉的故事封面"><div class="book-info"><div class="book-title">撒哈拉的故事</div><div class="book-meta">三毛 · 9成新 · 北京</div><div class="book-price">¥ 12.00 <button class="buy-btn" onclick="addToBag('撒哈拉的故事')">加入书袋</button></div></div></article>
                        <!-- 天才女友 -->
                        <article class="book-item"><img src="https://raw.githubusercontent.com/myrazanglin-art/Hometree-Social-App/main/images/天才.jpg" class="book-cover" alt="我的天才女友封面"><div class="book-info"><div class="book-title">我的天才女友</div><div class="book-meta">费兰特 · 8成新 · 上海</div><div class="book-price">¥ 18.50 <button class="buy-btn" onclick="addToBag('我的天才女友')">加入书袋</button></div></div></article>
                        <!-- np(正常人) -->
                        <article class="book-item"><img src="https://raw.githubusercontent.com/myrazanglin-art/Hometree-Social-App/main/images/np.jpg" class="book-cover" alt="正常人封面"><div class="book-info"><div class="book-title">正常人</div><div class="book-meta">萨莉·鲁尼 · 全新 · 广州</div><div class="book-price">¥ 25.00 <button class="buy-btn" onclick="addToBag('正常人')">加入书袋</button></div></div></article>
                        <!-- 百年孤独 -->
                        <article class="book-item"><img src="https://raw.githubusercontent.com/myrazanglin-art/Hometree-Social-App/main/images/百年.jpg" class="book-cover" alt="百年孤独封面"><div class="book-info"><div class="book-title">百年孤独</div><div class="book-meta">马尔克斯 · 7成新 · 杭州</div><div class="book-price">¥ 9.90 <button class="buy-btn" onclick="addToBag('百年孤独')">加入书袋</button></div></div></article>
                    </div>
                </div>
            </section>
            <section class="tab-page" id="page-community">
                <div class="page-inner">
                    <h1 class="page-heading">论坛</h1><p class="page-subheading">分享最近打动你的事。</p>
                    <div class="xhs-masonry">
                        <article class="xhs-card"><img src="https://raw.githubusercontent.com/myrazanglin-art/Hometree-Social-App/main/images/7.jpg" class="xhs-img" style="height:250px" alt="音乐现场"><div class="xhs-content">罗大佑的歌词，句句都是时代挽歌。</div><div class="xhs-author"><img src="https://raw.githubusercontent.com/myrazanglin-art/Hometree-Social-App/main/images/8.jpg" class="xhs-avatar" alt="">Yiming</div></article>
                        <article class="xhs-card"><img src="https://raw.githubusercontent.com/myrazanglin-art/Hometree-Social-App/main/images/8.jpg" class="xhs-img" style="height:180px" alt="电影与影像"><div class="xhs-content">重看《搏击俱乐部》，还是被 Tyler 震撼。</div><div class="xhs-author"><img src="https://raw.githubusercontent.com/myrazanglin-art/Hometree-Social-App/main/images/8.jpg" class="xhs-avatar" alt="">Yiming</div></article>
                        <article class="xhs-card"><img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600" class="xhs-img" style="height:220px" alt="抽象艺术"><div class="xhs-content">Björk 的现场是一场极光祭祀。</div><div class="xhs-author"><img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=60" class="xhs-avatar" alt="">Björk</div></article>
                    </div>
                </div>
            </section>
            <section class="tab-page" id="page-profile">
                <div class="page-inner">
                    <h1 class="page-heading">我的</h1>
                    <div class="profile-header"><img src="https://raw.githubusercontent.com/myrazanglin-art/Hometree-Social-App/main/images/avatar.jpg" class="avatar" alt="头像"><div><h2>Yiming</h2><p>豆瓣 126本在读 · 网易云 89首私藏</p></div></div>
                    <div class="settings-grid">
                        <div class="setting-card"><span>隐身模式（不被推荐）</span><div class="toggle active" role="switch" aria-checked="true" tabindex="0" onclick="toggleSwitch(this)" onkeydown="toggleOnKey(event,this)"></div></div>
                        <div class="setting-card"><span>屏蔽 / 拉黑管理</span><span class="setting-action" onclick="alert('已屏蔽 2 人')">查看（2）</span></div>
                        <div class="setting-card"><span>同步豆瓣书影音</span><span class="setting-action">已绑定</span></div>
                        <div class="setting-card"><span>同步网易云歌单</span><span style="color:var(--muted)">未绑定</span></div>
                    </div>
                </div>
            </section>
        </main>
        <nav class="bottom-nav" aria-label="主导航">
            <div class="nav-item active" role="button" tabindex="0" onclick="switchTab('page-match',this)" onkeydown="navOnKey(event,this)"><span class="nav-icon">⌕</span><span>匹配</span></div>
            <div class="nav-item" role="button" tabindex="0" onclick="switchTab('page-market',this)" onkeydown="navOnKey(event,this)"><span class="nav-icon">▤</span><span>书市</span></div>
            <div class="nav-item" role="button" tabindex="0" onclick="switchTab('page-community',this)" onkeydown="navOnKey(event,this)"><span class="nav-icon">✳</span><span>社区</span></div>
            <div class="nav-item" role="button" tabindex="0" onclick="switchTab('page-profile',this)" onkeydown="navOnKey(event,this)"><span class="nav-icon">◉</span><span>我的</span></div>
        </nav>
    </div>
    <section class="chat-modal" id="chatModal" aria-label="聊天">
        <header class="chat-header"><button class="back-btn" onclick="closeChat()" aria-label="返回">‹</button><img id="chatAvatar" class="chat-avatar" src="" alt=""><div class="chat-name" id="chatName"></div></header>
        <div class="chat-body" id="chatBody" aria-live="polite"></div>
        <div class="chat-input-area"><input class="chat-input" id="chatInput" placeholder="发消息..." aria-label="消息内容"><button class="send-btn" onclick="sendMessage()">发送</button></div>
    </section>
    <script>
        const users = [
            { id:"louye", name:"娄烨", age:58, img:"https://raw.githubusercontent.com/myrazanglin-art/Hometree-Social-App/main/images/1.jpg", tags:["苏州河","推拿"], quote:"如果有一天我走了...", ai:"适合在雨天聊贾宏声。" },
            { id:"tyler", name:"Tyler Durden", age:30, img:"https://raw.githubusercontent.com/myrazanglin-art/Hometree-Social-App/main/images/2.jpg", tags:["Fight Club","Nihilism"], quote:"You are not your job.", ai:"别聊工作，聊地下搏击。" },
            { id:"morrissey", name:"Morrissey", age:64, img:"https://raw.githubusercontent.com/myrazanglin-art/Hometree-Social-App/main/images/3.jpg", tags:["The Smiths","Indie"], quote:"There is a light...", ai:"深夜 emo 必备。" },
            { id:"bjork", name:"Björk", age:58, img:"https://raw.githubusercontent.com/myrazanglin-art/Hometree-Social-App/main/images/4.jpg", tags:["Art Pop","实验电子"], quote:"I'm the spark.", ai:"冰岛极光与实验电子。" },
            { id:"lotayu", name:"罗大佑", age:68, img:"https://raw.githubusercontent.com/myrazanglin-art/Hometree-Social-App/main/images/5.jpg", tags:["鹿港小镇","时代"], quote:"台北不是我的家。", ai:"午夜聊华语启蒙。" },
            { id:"emo", name:"Midwest Emo", age:22, img:"https://raw.githubusercontent.com/myrazanglin-art/Hometree-Social-App/main/images/6.jpg", tags:["Math Rock","Drop D"], quote:"Let's play in drop D.", ai:"效果器男孩。" },
            { id:"muse", name:"Matt Bellamy", age:45, img:"https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=600", tags:["Muse","Space Rock"], quote:"This is the last time.", ai:"科幻与反乌托邦。" },
            { id:"aphex", name:"Aphex Twin", age:52, img:"https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=600", tags:["IDM","Ambient"], quote:"Weird music.", ai:"Max/MSP 同好。" },
            { id:"kurt", name:"Kurt Cobain", age:27, img:"https://raw.githubusercontent.com/myrazanglin-art/Hometree-Social-App/main/images/7.jpg", tags:["Grunge","Nirvana"], quote:"I'd rather be hated.", ai:"聊聊地下厂牌。" },
            { id:"kevin", name:"Kevin Shields", age:60, img:"https://raw.githubusercontent.com/myrazanglin-art/Hometree-Social-App/main/images/8.jpg", tags:["Shoegaze","MBV"], quote:"Loveless is a wall.", ai:"噪音墙之神。" }
        ];
        let currentIndex = 0;
        let matchedUsers = JSON.parse(localStorage.getItem("hometree_matches") || "[]");
        let chatHistories = JSON.parse(localStorage.getItem("hometree_chats") || "{}");
        let activeChatId = null;
        let swipeLocked = false;
        const container = document.getElementById("cardContainer");

        function renderAll() {
            container.innerHTML = "";
            if (currentIndex >= users.length) {
                container.innerHTML = '<div class="empty-matches">暂时没有更多推荐，稍后再来看看。</div>';
            } else {
                for (let i = users.length - 1; i >= currentIndex; i--) {
                    const user = users[i];
                    const offset = i - currentIndex;
                    const card = document.createElement("article");
                    card.className = "swipe-card";
                    card.dataset.top = String(offset === 0);
                    card.style.transform = `scale(${1 - offset * .035}) translateY(${offset * 12}px)`;
                    card.style.zIndex = String(users.length - offset);
                    card.style.opacity = String(Math.max(.35, 1 - offset * .13));
                    card.innerHTML = `
                        <img src="${user.img}" class="card-img" alt="${user.name}">
                        <div class="card-info">
                            <div class="name-row"><div class="name"></div><div class="age">${user.age}</div></div>
                            <div class="tags">${user.tags.map(t => `<span class="tag"></span>`).join("")}</div>
                            <div class="media-links">
                                <button class="media-btn btn-douban" onclick="alert('跳转豆瓣查看：${user.tags[0]}')">豆瓣</button>
                                <button class="media-btn btn-netease" onclick="alert('跳转网易云查看：${user.tags[0]}')">网易云</button>
                            </div>
                            <div class="quote"></div><div class="ai-agent">✦ <span></span></div>
                        </div>`;
                    card.querySelector(".name").textContent = user.name;
                    card.querySelector(".quote").textContent = `“${user.quote}”`;
                    card.querySelector(".ai-agent span").textContent = `AI · ${user.ai}`;
                    card.querySelectorAll(".tag").forEach((tag, index) => tag.textContent = user.tags[index]);
                    container.appendChild(card);
                }
            }
            document.getElementById("matchesCount").textContent = `(${matchedUsers.length})`;
            const list = document.getElementById("matchesList");
            list.innerHTML = "";
            if (!matchedUsers.length) {
                list.innerHTML = '<div class="empty-matches">喜欢一位推荐对象，即可开始聊天。</div>';
            }
            matchedUsers.forEach(user => {
                const msgs = chatHistories[user.id] || [];
                const item = document.createElement("div");
                item.className = "match-item";
                item.tabIndex = 0;
                item.setAttribute("role", "button");
                const img = document.createElement("img");
                img.className = "match-avatar"; img.src = user.img; img.alt = "";
                const info = document.createElement("div"); info.className = "match-info";
                const name = document.createElement("div"); name.className = "match-name"; name.textContent = user.name;
                const last = document.createElement("div"); last.className = "match-last";
                last.textContent = msgs.length ? msgs[msgs.length - 1].text : "匹配成功，打个招呼吧！";
                info.append(name, last); item.append(img, info);
                item.onclick = () => openChat(user);
                item.onkeydown = event => { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); openChat(user); } };
                list.appendChild(item);
            });
            attachSwipe();
        }

        function swipe(direction) {
            if (currentIndex >= users.length || swipeLocked) return;
            const topCard = container.querySelector(".swipe-card[data-top='true']");
            if (!topCard) return;
            swipeLocked = true;
            const user = users[currentIndex];
            topCard.style.transform = direction === "right" ? "translate3d(125%,0,0) rotate(15deg)" : "translate3d(-125%,0,0) rotate(-15deg)";
            topCard.style.opacity = "0";
            if (direction === "right" && !matchedUsers.some(item => item.id === user.id)) {
                matchedUsers.push(user);
                if (!chatHistories[user.id]) chatHistories[user.id] = [];
                saveState();
            }
            currentIndex++;
            window.setTimeout(() => {
                renderAll();
                swipeLocked = false;
                if (direction === "right") openChat(user);
            }, 300);
        }

        function attachSwipe() {
            const card = container.querySelector(".swipe-card[data-top='true']");
            if (!card) return;
            let startX = 0, startY = 0, deltaX = 0, dragging = false;
            card.addEventListener("pointerdown", event => {
                if (event.target.closest("button")) return;
                startX = event.clientX; startY = event.clientY; deltaX = 0; dragging = true;
                card.setPointerCapture(event.pointerId);
                card.style.transition = "none";
            });
            card.addEventListener("pointermove", event => {
                if (!dragging) return;
                deltaX = event.clientX - startX;
                if (Math.abs(deltaX) > Math.abs(event.clientY - startY)) {
                    card.style.transform = `translate3d(${deltaX}px,${Math.min(18, Math.abs(deltaX) * .025)}px,0) rotate(${deltaX * .035}deg)`;
                }
            });
            const finish = () => {
                if (!dragging) return;
                dragging = false;
                card.style.transition = "";
                if (Math.abs(deltaX) > Math.min(90, window.innerWidth * .22)) swipe(deltaX > 0 ? "right" : "left");
                else { card.style.transform = ""; }
            };
            card.addEventListener("pointerup", finish);
            card.addEventListener("pointercancel", finish);
        }

        function openChat(user) {
            activeChatId = user.id;
            document.getElementById("chatName").textContent = user.name;
            document.getElementById("chatAvatar").src = user.img;
            document.getElementById("chatModal").style.display = "flex";
            document.getElementById("chatInput").focus({ preventScroll: true });
            renderChatMessages();
        }
        function closeChat() {
            document.getElementById("chatModal").style.display = "none";
            activeChatId = null;
            renderAll();
        }
        function renderChatMessages() {
            const body = document.getElementById("chatBody");
            body.innerHTML = "";
            const messages = chatHistories[activeChatId] || [];
            if (!messages.length) {
                addMessageToDB(activeChatId, "Hey，很高兴匹配到你。", "left");
                return;
            }
            messages.forEach(message => {
                const div = document.createElement("div");
                div.className = `msg msg-${message.type}`;
                div.textContent = message.text;
                body.appendChild(div);
            });
            body.scrollTop = body.scrollHeight;
        }
        function addMessageToDB(id, text, type) {
            if (!chatHistories[id]) chatHistories[id] = [];
            chatHistories[id].push({ text, type });
            saveState();
            if (activeChatId === id) renderChatMessages();
        }
        function sendMessage() {
            const input = document.getElementById("chatInput");
            const text = input.value.trim();
            if (!text || !activeChatId) return;
            const chatId = activeChatId;
            addMessageToDB(chatId, text, "right");
            input.value = "";
            window.setTimeout(() => {
                if (chatHistories[chatId]) addMessageToDB(chatId, "我也这么觉得，这就是我们在这里相遇的原因。", "left");
            }, 1000);
        }
        function saveState() {
            localStorage.setItem("hometree_matches", JSON.stringify(matchedUsers));
            localStorage.setItem("hometree_chats", JSON.stringify(chatHistories));
            renderAll();
        }
        function switchTab(pageId, button) {
            document.querySelectorAll(".tab-page").forEach(page => page.classList.toggle("active", page.id === pageId));
            document.querySelectorAll(".nav-item").forEach(item => item.classList.toggle("active", item === button));
        }
        function navOnKey(event, element) {
            if (event.key === "Enter" || event.key === " ") { event.preventDefault(); element.click(); }
        }
        function toggleTheme() {
            const body = document.body;
            const next = body.dataset.theme === "light" ? "dark" : "light";
            body.dataset.theme = next;
            localStorage.setItem("hometree_theme", next);
            updateThemeButton();
        }
        function updateThemeButton() {
            const dark = document.body.dataset.theme === "dark";
            document.getElementById("themeIcon").textContent = dark ? "☀" : "☾";
            document.getElementById("themeLabel").textContent = dark ? "light mode" : "night mode";
        }
        function toggleSwitch(element) {
            element.classList.toggle("active");
            element.setAttribute("aria-checked", String(element.classList.contains("active")));
        }
        function toggleOnKey(event, element) {
            if (event.key === "Enter" || event.key === " ") { event.preventDefault(); toggleSwitch(element); }
        }
        function addToBag(title) { alert(`《${title}》已加入书袋`); }
        document.getElementById("chatInput").addEventListener("keydown", event => { if (event.key === "Enter") sendMessage(); });
        document.addEventListener("keydown", event => { if (event.key === "Escape" && activeChatId) closeChat(); });
        const savedTheme = localStorage.getItem("hometree_theme");
        if (savedTheme === "dark") document.body.dataset.theme = "dark";
        updateThemeButton();
        renderAll();
    </script>
</body>
</html>
"""

components.html(html_code, height=1000, scrolling=False)
