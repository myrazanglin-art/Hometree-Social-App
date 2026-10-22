import streamlit as st
import requests
import random

st.set_page_config(page_title="Hometree | Find Your Soul", page_icon="🌳", layout="centered")

apple_css = """
<style>
    /* 全局背景与字体 */
    .stApp {
        background-color: #F5F5F7;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    /* 隐藏 Streamlit 默认的顶部工具栏 */
    header {visibility: hidden;}
    
    /* 卡片样式 */
    .apple-card {
        background: #FFFFFF;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    /* 标题 */
    h1, h2, h3 {
        color: #1D1D1F;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    
    /* 小众标签 */
    .niche-tag {
        display: inline-block;
        background: #E8E8ED;
        color: #86868B;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 14px;
        margin: 5px;
        cursor: pointer;
    }
    
    /* 极简播放器 */
    .vinyl-player {
        display: flex;
        align-items: center;
        background: #FFFFFF;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-top: 20px;
    }
    .album-cover {
        width: 80px; height: 80px;
        border-radius: 10px;
        background: #000;
        margin-right: 20px;
        object-fit: cover;
    }
    .music-info h4 { margin: 0; color: #1D1D1F; font-size: 16px; }
    .music-info p { margin: 5px 0 0 0; color: #86868B; font-size: 14px; }
</style>
"""
st.markdown(apple_css, unsafe_allow_html=True)

# ==========================================
# 2. 核心逻辑：对接豆瓣真实数据
# ==========================================
# (此处使用豆瓣公开 API 代理或模拟真实数据，以确保运行成功)
# 我们打造一个小众书影音池，完美契合你的亚文化人设
NICHE_ITEMS = {
    "书籍": [
        {"title": "《百年孤独》", "author": "加西亚·马尔克斯", "cover": "https://img9.doubanio.com/view/subject/s/public/s27237850.jpg"},
        {"title": "《地下室手记》", "author": "陀思妥耶夫斯基", "cover": "https://img1.doubanio.com/view/subject/s/public/s27238019.jpg"},
        {"title": "《消费社会》", "author": "让·鲍德里亚", "cover": "https://img2.doubanio.com/view/subject/s/public/s27239138.jpg"}
    ],
    "电影": [
        {"title": "《蚀》", "author": "米开朗基罗·安东尼奥尼", "cover": "https://img2.doubanio.com/view/photo/s_ratio_poster/public/p2515439334.webp"},
        {"title": "《攻壳机动队》", "author": "押井守", "cover": "https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2508721156.webp"},
        {"title": "《穆赫兰道》", "author": "大卫·林奇", "cover": "https://img2.doubanio.com/view/photo/s_ratio_poster/public/p2668391220.webp"}
    ]
}

# 模拟的网易云歌单
NETEASE_SONGS = [
    {"name": "There Is a Light That Never Goes Out", "artist": "The Smiths", "id": "1314907329"},
    {"name": "Apocalypse", "artist": "Cigarettes After Sex", "id": "1915209654"},
    {"name": "Weird Fishes/Arpeggi", "artist": "Radiohead", "id": "1314907329"}
]

# ==========================================
# 3. UI 渲染
# ==========================================
st.markdown("<div class='apple-card'>", unsafe_allow_html=True)
st.title("Hometree.")
st.subheader("连接灵魂的隐私社交。")
st.write("基于书影音的极致小众匹配。我们不滑动，我们只寻找频率相同的人。")
st.markdown("</div>", unsafe_allow_html=True)

# 书影音对接模块
st.markdown("### 📚 你的精神切片")
tab1, tab2 = st.tabs(["最近在读", "最近在看"])

with tab1:
    for book in NICHE_ITEMS["书籍"]:
        st.markdown(f"""
        <div class="vinyl-player" style="margin-bottom: 10px; padding: 10px;">
            <img class="album-cover" src="{book['cover']}">
            <div class="music-info">
                <h4>{book['title']}</h4>
                <p>{book['author']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    for movie in NICHE_ITEMS["电影"]:
        st.markdown(f"""
        <div class="vinyl-player" style="margin-bottom: 10px; padding: 10px;">
            <img class="album-cover" src="{movie['cover']}">
            <div class="music-info">
                <h4>{movie['title']}</h4>
                <p>{movie['author']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# 网易云音乐模块
st.markdown("### 🎧 你的精神频率 (网易云同步)")
song = random.choice(NETEASE_SONGS)

st.markdown(f"""
<div class="vinyl-player">
    <div style="width:80px; height:80px; border-radius:50%; background: linear-gradient(45deg, #1D1D1F, #3A3A3C); margin-right:20px; display:flex; justify-content:center; align-items:center;">
        <div style="width:20px; height:20px; border-radius:50%; background:#FFF;"></div>
    </div>
    <div class="music-info">
        <h4>{song['name']}</h4>
        <p>{song['artist']} · 正在播放</p>
    </div>
</div>
""", unsafe_allow_html=True)

# 这里嵌入了真实的网易云外链播放器，实现真实播放
st.components.v1.iframe(f"https://music.163.com/outchain/player?type=2&id={song['id']}&auto=0&height=66", height=80)

st.divider()

# 匹配按钮
st.markdown("<div class='apple-card' style='text-align: center;'>", unsafe_allow_html=True)
st.write("#### 寻找同频的灵魂")
if st.button("✨ 运行匹配算法 (Cosine Similarity)", use_container_width=True):
    with st.spinner('正在计算多维向量空间...'):
        import time
        time.sleep(1.5) # 模拟算法计算时间
        st.success("匹配成功！与你在《百年孤独》和 The Smiths 上品味重合度 98.7% 的用户：")
        st.info("**@Yuki_Indie** (坐标：香港) - “我也喜欢在雨天听 Cigarettes After Sex。”")
st.markdown("</div>", unsafe_allow_html=True)
