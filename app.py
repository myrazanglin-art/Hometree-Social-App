import os
from urllib.parse import quote
from typing import Any, Dict, List

import streamlit as st

try:
    import mysql.connector
    MYSQL_DRIVER_AVAILABLE = True
except ImportError:
    mysql = None
    MYSQL_DRIVER_AVAILABLE = False

st.set_page_config(page_title="Hometree", page_icon="📚", layout="wide")


def fallback_avatar(name: str, accent: str = "7C3AED") -> str:
    initials = "".join(part[0].upper() for part in name.split()[:2] if part)
    if not initials:
        initials = "H"
    return (
        f"https://ui-avatars.com/api/?name={quote(initials)}"
        f"&background={accent}&color=fff&size=200"
    )


def mysql_available() -> bool:
    if not MYSQL_DRIVER_AVAILABLE:
        return False
    try:
        config = {
            "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
            "port": int(os.getenv("MYSQL_PORT", "3306")),
            "database": os.getenv("MYSQL_DATABASE", "hometree"),
            "user": os.getenv("MYSQL_USER", "root"),
            "password": os.getenv("MYSQL_PASSWORD", ""),
            "autocommit": True,
        }
        conn = mysql.connector.connect(**config)
        conn.close()
        return True
    except Exception:
        return False


st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #f5efe8 0%, #f7f1f6 30%, #eef4f7 100%);
            color: #1f2937;
        }

        .stApp {
            background: linear-gradient(135deg, #f5efe8 0%, #f7f1f6 30%, #eef4f7 100%);
        }

        .block-container {
            max-width: 1480px;
            padding-top: 1.8rem;
            padding-bottom: 2rem;
        }

        [data-testid="stSidebar"] {
            background: rgba(255,255,255,0.55);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            border-right: 1px solid rgba(124, 58, 237, 0.08);
        }

        .stTabs [role="tablist"] {
            gap: 0.5rem;
        }

        .stTabs [role="tab"] {
            border-radius: 12px;
            padding: 0.5rem 0.9rem;
            color: #374151;
            font-weight: 600;
        }

        .stTabs [role="tab"][aria-selected="true"] {
            background: rgba(124, 58, 237, 0.1);
            color: #4c1d95;
        }

        div[data-testid="stMetricValue"] {
            font-size: 1.2rem;
            font-weight: 700;
        }

        .glass-card {
            background: rgba(255,255,255,0.66);
            border: 1px solid rgba(31, 41, 55, 0.06);
            border-radius: 26px;
            padding: 1rem;
            box-shadow: 0 16px 28px rgba(15, 23, 42, 0.08);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            margin-bottom: 1rem;
        }

        .hero-panel {
            background:
                linear-gradient(120deg, rgba(255,255,255,0.18), rgba(124,58,237,0.08)),
                url('https://images.unsplash.com/photo-1521587760476-6c12a4b040da?auto=format&fit=crop&w=1200&q=80') center/cover no-repeat;
            border-radius: 30px;
            padding: 1.2rem;
            min-height: 200px;
            border: 1px solid rgba(255,255,255,0.3);
            box-shadow: 0 16px 30px rgba(128, 90, 213, 0.12);
        }

        .hero-title {
            font-size: clamp(2rem, 2.8vw, 3rem);
            font-weight: 800;
            color: #111827;
            margin-top: 1rem;
        }

        .soft-pill {
            display: inline-block;
            padding: 0.42rem 0.75rem;
            background: rgba(255,255,255,0.7);
            color: #374151;
            border-radius: 999px;
            border: 1px solid rgba(15, 23, 42, 0.06);
            font-size: 0.78rem;
            font-weight: 600;
            margin: 0.15rem 0.35rem 0.2rem 0;
        }

        .book-cover,
        .media-cover,
        .podcast-cover {
            border-radius: 20px;
            box-shadow: 0 10px 22px rgba(15, 23, 42, 0.12);
            object-fit: cover;
        }

        .mini-avatar {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            object-fit: cover;
            border: 2px solid rgba(255,255,255,0.8);
        }

        .compact-card {
            background: rgba(255,255,255,0.68);
            border: 1px solid rgba(15, 23, 42, 0.06);
            border-radius: 20px;
            padding: 0.75rem 0.85rem;
            box-shadow: 0 10px 16px rgba(15, 23, 42, 0.04);
        }

        .forum-item:hover,
        .card-shell:hover {
            transform: translateY(-1px);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .stButton > button {
            border-radius: 14px;
            border: none;
            color: #ffffff;
            background: linear-gradient(135deg, #1f2937 0%, #4b5563 100%);
            font-weight: 600;
            padding: 0.65rem 1rem;
            box-shadow: 0 8px 18px rgba(31, 41, 55, 0.14);
        }

        .stButton > button:hover {
            filter: brightness(1.03);
            transform: translateY(-1px);
        }

        .secondary-btn > button {
            background: rgba(255,255,255,0.7) !important;
            color: #1f2937 !important;
            border: 1px solid rgba(15, 23, 42, 0.08);
            box-shadow: none;
        }

        @media (max-width: 768px) {
            .block-container {
                padding-left: 0.7rem;
                padding-right: 0.7rem;
            }
            .hero-panel {
                min-height: 180px;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def seed_data() -> Dict[str, Any]:
    return {
        "profile": {
            "name": "Yiming",
            "avatar": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=900&q=80",
            "bio": "to be or not to be.",
            "location": "上海",
            "social": {
                "douban": "豆瓣：已绑定· 126 条读过",
                "netease": "网易云：最近在听《浮躁》、techno",
            },
            "highlights": [
                "喜欢安静的独立出版",
                "收藏偏电影与文学的城市叙事",
                "正在读《看见》《精神疾病与心理学》",
            ],
        },
        "users": [
            {
                "id": "louye",
                "name": "67小子",
                "age": 28,
                "img": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&w=900&q=80",
                "tags": ["67", "67", "67"],
                "quote": "six seven",
                "ai": "网感少萝。",
                "douban": "豆瓣：已收藏 132 本书与 96 部电影",
                "netease": "网易云：最爱爵士。",
            },
            {
                "id": "bjork",
                "name": "冰岛宝马",
                "age": 34,
                "img": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=900&q=80",
                "tags": ["Art Pop", "电子", "视觉艺术"],
                "quote": "I am the spark, and the sound is my map.",
                "ai": "在艺术和音乐之间来回穿梭，喜欢具有实验性的表达。",
                "douban": "豆瓣：蓝色妖姬",
                "netease": "网易云：电子、实验和氛围音乐收藏夹",
            },
            {
                "id": "tyler",
                "name": "Tyler Durden",
                "age": 30,
                "img": "https://images.unsplash.com/photo-1520637836862-4d197d17c90a?auto=format&fit=crop&w=900&q=80",
                "tags": ["Fight Club", "荒诞", "反主流"],
                "quote": "You are not your job.",
                "ai": "如果我是布拉德皮特你会爱我吗。",
                "douban": "豆瓣：地域文化与电影史有较深关注",
                "netease": "网易云：重度摇滚与冷门独立歌单",
            },
            {
                "id": "lotayu",
                "name": "dj小女孩",
                "age": 27,
                "img": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=900&q=80",
                "tags": ["治愈", "旅行", "日记"],
                "quote": "旅行是为了重新认识自己的生活方式。",
                "ai": "喜欢轻旅行、摄影和缓慢型音乐，日记本比社交软件更真实。",
                "douban": "豆瓣：旅行笔记、图书、电影记录很全",
                "netease": "网易云：温暖治愈与城市散步歌单",
            },
        ],
        "books": [
            {
                "id": 1,
                "title": "活着",
                "author": "余华",
                "price": 18.9,
                "city": "杭州",
                "cover": "https://img1.doubanio.com/view/subject/s/public/s27214154.jpg",
                "tags": ["现实主义", "中国文学"],
                "similar": ["许三观卖血记", "兄弟", "白鹿原"],
                "summary": "福贵的一生像一场跨越时代的苦难记录，荒诞中透着热烈的生命力。",
            },
            {
                "id": 2,
                "title": "岛上书店",
                "author": "加·泽文",
                "price": 39.0,
                "city": "上海",
                "cover": "https://img9.doubanio.com/view/subject/s/public/s29810488.jpg",
                "tags": ["治愈", "小说"],
                "similar": ["晚熟的人", "一句顶一万句", "当呼吸化作风"],
                "summary": "在一个与世隔绝的小岛上，一间书店像一座灯塔，让人重新学会爱与失去。",
            },
            {
                "id": 3,
                "title": "人生海海",
                "author": "麦家",
                "price": 52.0,
                "city": "北京",
                "cover": "https://img1.doubanio.com/view/subject/s/public/s33939677.jpg",
                "tags": ["悬疑", "成长"],
                "similar": ["白夜行", "尘埃落定", "许三观卖血记"],
                "summary": "以一个极端的命运故事，放大人性里的善、恶与复杂的自我选择。",
            },
            {
                "id": 4,
                "title": "小王子",
                "author": "安托万·德·圣-埃克苏佩里",
                "price": 22.5,
                "city": "苏州",
                "cover": "https://img1.doubanio.com/view/subject/s/public/s1001902.jpg",
                "tags": ["童话", "哲思"],
                "similar": ["夜间飞行", "牧羊少年的奇幻之旅", "我在未来等你"],
                "summary": "一场关于爱、责任与成人世界的轻盈而深沉对话。",
            },
            {
                "id": 5,
                "title": "天才女友",
                "author": "苏打绿·今何在",
                "price": 34.0,
                "city": "深圳",
                "cover": "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=900&q=80",
                "tags": ["青春", "成长", "文学"],
                "similar": ["房思琪的初恋乐园", "向左走·向右走", "你好，旧时光"],
                "summary": "关于青春、才华与关系的温柔、尖锐又真实的书写。",
            },
            {
                "id": 6,
                "title": "房思琪的初恋乐园",
                "author": "林奕含",
                "price": 36.0,
                "city": "深圳",
                "cover": "https://img9.doubanio.com/view/subject/s/public/s28065015.jpg",
                "tags": ["文学", "成长"],
                "similar": ["围城", "我们的三十年", "失踪的孩子"],
                "summary": "一段关于青春创伤与自我救赎的书写，在极致的情绪里发光。",
            },
        ],
        "articles": [
            {
                "id": 101,
                "title": "如何在城市里把一本书读完？",
                "category": "阅读札记",
                "cover": "https://images.unsplash.com/photo-1516280440502-863a346513c1?auto=format&fit=crop&w=1200&q=80",
                "summary": "从地铁通勤到夜晚独处，一套低压力的阅读习惯设计。",
                "content": "如果你想真正读完一本书，不需要强迫自己每天写阅读计划，而是从固定的场景入手：搭乘地铁时读短篇，晚上在床头读长篇，周末把阅读变成有仪式感的短时段放空。我的经验是，把阅读当作一种生活习惯而不是任务，才能长久。",
            },
            {
                "id": 102,
                "title": "7个适合慢节奏生活的城市歌单",
                "category": "音乐笔记",
                "cover": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=1200&q=80",
                "summary": "从晨跑歌单到夜晚散步，找到适合自己的音乐频率。",
                "content": "我一直认为一张歌单最重要的，不是“有多少首歌”，而是“你愿意在哪种情境里听它”。早上适合温暖的民谣，晚上适合低频电子，雨天适合钢琴和城市灵魂歌。",
            },
            {
                "id": 103,
                "title": "我的旧书店清单：从书页到灯光",
                "category": "城市观察",
                "cover": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?auto=format&fit=crop&w=1200&q=80",
                "summary": "旧书店最打动人的地方，是书架后的暗色温度和人的慢节奏。",
                "content": "每次走进旧书店，都会自然放慢脚步。人们在棚架之间翻书，像在悄悄更新自己的人生地图。不同于快节奏电商，旧书店的魅力在于偶遇与不急切。",
            },
        ],
        "podcasts": [
            {
                "id": 201,
                "title": "《城市夜归》：一场夜跑前的温柔降噪",
                "host": "Yiming",
                "cover": "https://images.unsplash.com/photo-1511379938547-c1f69419868d?auto=format&fit=crop&w=1200&q=80",
                "summary": "12 分钟的夜晚散步声景，带着轻微电子与民谣的呼吸感。",
                "duration": "12:38",
                "src": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
                "type": "podcast",
            },
            {
                "id": 202,
                "title": "书店漫谈：旧书与温度",
                "host": "楼野",
                "cover": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?auto=format&fit=crop&w=1200&q=80",
                "summary": "从旧书店到独立影院，谈谈阅读与城市的关系。",
                "duration": "18:25",
                "src": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
                "type": "podcast",
            },
            {
                "id": 203,
                "title": "晚安读书会：一本书如何改变一段生活",
                "host": "洛塔雨",
                "cover": "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?auto=format&fit=crop&w=1200&q=80",
                "summary": "一本好书不是答案，而是让你更清楚看见自己。",
                "duration": "15:02",
                "src": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
                "type": "podcast",
            },
        ],
        "forum_threads": [
            {
                "id": 301,
                "title": "你最近都在读什么？来推荐一本让人愿意反复翻的书",
                "tag": "阅读",
                "meta": "18 小时前 · 12 回复",
                "desc": "无论是城市故事、文学长篇，还是短篇文集，都想听听你最近的阅读体验。",
            },
            {
                "id": 302,
                "title": "今晚发一档很适合散步的播客：城市夜归",
                "tag": "播客",
                "meta": "26 小时前 · 21 回复",
                "desc": "想知道大家会用什么歌单陪散步、陪雨夜、陪写作，我想做一个慢节奏清单。",
            },
            {
                "id": 303,
                "title": "旧书店线下小组：你去过哪些值得反复回访的地方？",
                "tag": "社区",
                "meta": "11 小时前 · 9 回复",
                "desc": "分享你最喜欢的旧书店、街角咖啡和安静到能听见翻页声的地方。",
            },
        ],
        "forum_replies": {
            301: [
                {"user": "夏夜", "text": "最近在读《活着》，感觉它的力量在于把悲伤写得极其克制，却又特别动人。"},
                {"user": "远山", "text": "我推荐《房思琪的初恋乐园》，它很痛，但也让人更认真地看待文学与创伤。"},
            ],
            302: [
                {"user": "Mina", "text": "我会用《城市夜归》作为夜跑的歌单，氛围很适合静下来。"},
                {"user": "赫兹", "text": "雨天听民谣和电子混合，像一部城市电影的BGM。"},
            ],
            303: [
                {"user": "阿春", "text": "最喜欢的还是南边那家老书店，灯光很暖，书页香味特别真实。"},
                {"user": "柯西", "text": "我最近一直在找有悠长书架和咖啡的地方，最重要是别太吵。"},
            ],
        },
    }


def get_data() -> Dict[str, Any]:
    data = seed_data()
    if not MYSQL_DRIVER_AVAILABLE or not mysql_available():
        st.caption("MySQL 未配置，当前使用本地演示数据。")
        return data

    try:
        if not MYSQL_DRIVER_AVAILABLE:
            raise RuntimeError("MySQL driver is not available")

        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "127.0.0.1"),
            port=int(os.getenv("MYSQL_PORT", "3306")),
            database=os.getenv("MYSQL_DATABASE", "hometree"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            autocommit=True,
        )
        with conn.cursor(dictionary=True) as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS app_books (
                    id INT PRIMARY KEY,
                    title VARCHAR(255),
                    author VARCHAR(255),
                    price DECIMAL(10,2),
                    city VARCHAR(100),
                    cover VARCHAR(512),
                    tags JSON,
                    similar JSON,
                    summary TEXT
                )
                """
            )
            cur.execute("SELECT COUNT(*) AS total FROM app_books")
            if cur.fetchone()["total"] == 0:
                for book in data["books"]:
                    cur.execute(
                        "INSERT INTO app_books (id, title, author, price, city, cover, tags, similar, summary) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (
                            book["id"],
                            book["title"],
                            book["author"],
                            float(book["price"]),
                            book["city"],
                            book["cover"],
                            book["tags"],
                            book["similar"],
                            book["summary"],
                        ),
                    )
            cur.execute("SELECT * FROM app_books ORDER BY id")
            rows = cur.fetchall()
            if rows:
                data["books"] = rows
                for book in data["books"]:
                    book["tags"] = book["tags"] or []
                    book["similar"] = book["similar"] or []
        conn.close()
        st.caption("MySQL 连接成功，已加载数据库数据。")
    except Exception:
        st.caption("MySQL 未配置或连接失败，当前使用本地演示数据。")
    return data


def render_chat_panel(user: Dict[str, Any]) -> None:
    with st.sidebar:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader(f"聊天 · {user['name']}")
        st.image(user.get("img") or fallback_avatar(user["name"]), width=70)
        st.caption(user.get("douban", ""))
        st.caption(user.get("netease", ""))

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = {}

        for msg in st.session_state.chat_history.get(user["id"], []):
            if msg["role"] == "assistant":
                with st.chat_message("assistant"):
                    st.write(msg["text"])
            else:
                with st.chat_message("user"):
                    st.write(msg["text"])

        prompt = st.chat_input("给对方发一句话…")
        if prompt:
            history = st.session_state.chat_history.setdefault(user["id"], [])
            history.append({"role": "user", "text": prompt})
            history.append({"role": "assistant", "text": "我挺喜欢你的书单和梳理方式，下一本书我想先试试你最近在看的那种。"})
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


def render_match_tab(data: Dict[str, Any]) -> None:
    st.title("匹配")
    st.caption("根据书影音、阅读和音乐偏好筛选更匹配的朋友。")

    if "match_index" not in st.session_state:
        st.session_state.match_index = 0
    if "matched_users" not in st.session_state:
        st.session_state.matched_users = []
    if "selected_match" not in st.session_state:
        st.session_state.selected_match = None

    users = data["users"]
    if st.session_state.match_index >= len(users):
        st.session_state.match_index = 0

    left, right = st.columns([2.1, 1.0])
    with left:
        user = users[st.session_state.match_index]
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.image(user["img"], use_container_width=True, clamp=True)
        st.subheader(user["name"])
        st.caption(f"{user['age']} 岁 · {' / '.join(user['tags'])}")
        st.markdown(f"> {user['quote']}")
        st.write(user["ai"])

        match_bar = st.progress(72)
        st.caption("匹配度：72%")

        col_a, col_b = st.columns(2)
        if col_a.button("♥ 想认识", use_container_width=True):
            if user["id"] not in [u["id"] for u in st.session_state.matched_users]:
                st.session_state.matched_users.append(user)
            st.session_state.selected_match = user
            st.session_state.match_index += 1
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = {}
            st.session_state.chat_history.setdefault(
                user["id"],
                [{"role": "assistant", "text": "你好，我挺喜欢你的阅读列表和歌单风格，想聊聊下一本书。"}],
            )
            st.rerun()

        if col_b.button("✕ 下一位", use_container_width=True):
            st.session_state.match_index += 1
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("已匹配")
        if not st.session_state.matched_users:
            st.info("还没有匹配到朋友，先看看下一位。")
        for u in st.session_state.matched_users:
            row = st.columns([1, 4])
            with row[0]:
                st.image(u["img"], width=52)
            with row[1]:
                if st.button(u["name"], key=f"match_{u['id']}", use_container_width=True):
                    st.session_state.selected_match = u
                    st.rerun()
                past = st.session_state.chat_history.get(u["id"], [])
                text = past[-1]["text"] if past else "最近很想聊聊书和音乐。"
                st.caption(text[:30])
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.selected_match is not None:
        render_chat_panel(st.session_state.selected_match)


def render_market_tab(data: Dict[str, Any]) -> None:
    st.title("售卖书籍")
    st.caption("精选书单，带有封面、简介和相似推荐。")

    books = data["books"]
    grid = st.columns(3)
    for idx, book in enumerate(books):
        with grid[idx % 3]:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.image(book["cover"], use_container_width=True, output_format="JPEG")
            st.subheader(book["title"])
            st.caption(f"{book['author']} · {book['city']}")
            st.markdown(f"<div class='soft-pill'>¥{book['price']:.2f}</div>", unsafe_allow_html=True)
            for tag in book["tags"][:2]:
                st.markdown(f"<span class='soft-pill'>{tag}</span>", unsafe_allow_html=True)
            st.write(book["summary"])
            if st.button("详情", key=f"detail_{book['id']}", use_container_width=True):
                st.session_state.selected_book = book
            if st.button("加入清单", key=f"bag_{book['id']}", use_container_width=True):
                st.toast(f"已加入《{book['title']}》")
            st.markdown('</div>', unsafe_allow_html=True)

    if "selected_book" in st.session_state:
        book = st.session_state.selected_book
        st.divider()
        st.subheader(f"《{book['title']}》详情")
        col1, col2 = st.columns([1, 2])
        col1.image(book["cover"], use_container_width=True)
        with col2:
            st.markdown(f"**作者：** {book['author']}")
            st.markdown(f"**标签：** {' / '.join(book['tags'])}")
            st.markdown(f"**价格：** ¥{book['price']:.2f}")
            st.markdown(f"**简介：** {book['summary']}")
            st.markdown(f"**相似书：** {' · '.join(book['similar'])}")


def render_dynamic_tab(data: Dict[str, Any]) -> None:
    st.title("动态")
    article_tab, podcast_tab = st.tabs(["文章", "播客"])

    with article_tab:
        for post in data["articles"]:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.image(post["cover"], use_container_width=True)
            st.subheader(post["title"])
            st.caption(f"{post['category']} · 2 分钟阅读")
            st.write(post["summary"])
            if st.button("查看详情", key=f"article_{post['id']}", use_container_width=True):
                st.session_state.selected_article = post
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        if "selected_article" in st.session_state:
            post = st.session_state.selected_article
            st.divider()
            st.subheader(post["title"])
            st.caption(post["category"])
            st.write(post["content"])

    with podcast_tab:
        for pod in data["podcasts"]:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.image(pod["cover"], use_container_width=True)
            st.subheader(pod["title"])
            st.caption(f"{pod['host']} · {pod['duration']}")
            st.write(pod["summary"])
            if st.button("播放节目", key=f"pod_{pod['id']}", use_container_width=True):
                st.session_state.selected_podcast = pod
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        if "selected_podcast" in st.session_state:
            pod = st.session_state.selected_podcast
            st.divider()
            st.subheader(pod["title"])
            st.caption(f"主持：{pod['host']} · 时长：{pod['duration']}")
            st.audio(pod.get("src", ""), format="audio/mp3")


def render_forum_tab(data: Dict[str, Any]) -> None:
    st.title("论坛")
    st.caption("可定制的小型社区，内容可点开查看回复。")

    for thread in data["forum_threads"]:
        st.markdown('<div class="glass-card forum-item">', unsafe_allow_html=True)
        st.caption(thread["tag"])
        st.subheader(thread["title"])
        st.write(thread["desc"])
        st.caption(thread["meta"])
        c1, c2, c3 = st.columns([1, 1, 1])
        if c1.button("查看话题", key=f"forum_{thread['id']}", use_container_width=True):
            st.session_state.selected_forum = thread["id"]
            st.rerun()
        c2.button("回复数", key=f"replies_{thread['id']}", use_container_width=True)
        c3.button("收藏", key=f"favorite_{thread['id']}", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if "selected_forum" in st.session_state:
        thread_id = st.session_state.selected_forum
        thread = next(t for t in data["forum_threads"] if t["id"] == thread_id)
        st.divider()
        st.subheader(f"主题：{thread['title']}")
        st.write(thread["desc"])
        if thread_id in data["forum_replies"]:
            for reply in data["forum_replies"].get(thread_id, []):
                with st.chat_message("assistant"):
                    st.write(f"{reply['user']}：{reply['text']}")
        prompt = st.chat_input("写回复…")
        if prompt:
            data["forum_replies"].setdefault(thread_id, []).append({"user": "你", "text": prompt})
            st.rerun()


def render_profile_tab(data: Dict[str, Any]) -> None:
    profile = data["profile"]
    st.title("个人主页")

    st.markdown('<div class="hero-panel">', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 3])
    with c1:
        st.image(profile["avatar"], width=180)
    with c2:
        st.markdown(f'<div class="hero-title">{profile["name"]}</div>', unsafe_allow_html=True)
        st.caption(f"{profile['location']} · 已绑定豆瓣 / 网易云")
        st.write(profile["bio"])
    st.markdown('</div>', unsafe_allow_html=True)

    info_cols = st.columns(3)
    info_cols[0].metric("收藏", "126")
    info_cols[1].metric("听歌", "89")
    info_cols[2].metric("已读", "18")

    st.subheader("社交绑定")
    c1, c2 = st.columns(2)
    c1.info(profile["social"]["douban"])
    c2.info(profile["social"]["netease"])

    row = st.columns(2)
    row[0].button("绑定豆瓣", use_container_width=True)
    row[1].button("绑定网易云", use_container_width=True)

    st.subheader("主页定制")
    st.toggle("显示书影音偏好", value=True)
    st.toggle("显示音乐日记", value=True)
    st.toggle("显示书店收藏", value=True)

    st.subheader("兴趣标签")
    st.markdown(" ".join(f'<span class="soft-pill">{tag}</span>' for tag in profile["highlights"]), unsafe_allow_html=True)

    st.subheader("正在听")
    podcast = data["podcasts"][0]
    cover_col, info_col = st.columns([1, 3])
    cover_col.image(podcast["cover"], width=120)
    with info_col:
        st.write(f"**{podcast['title']}**")
        st.caption(f"{podcast['host']} · {podcast['duration']}")
        st.progress(62)
        p1, p2, p3 = st.columns(3)
        p1.button("▶ 播放", key="play_demo", use_container_width=True)
        p2.button("⏸ 暂停", key="pause_demo", use_container_width=True)
        p3.button("⏭ 下一首", key="next_demo", use_container_width=True)


pages = {
    "匹配": render_match_tab,
    "售卖": render_market_tab,
    "动态": render_dynamic_tab,
    "论坛": render_forum_tab,
    "主页": render_profile_tab,
}


def main() -> None:
    data = get_data()
    nav = st.sidebar.radio("导航", list(pages.keys()), index=0)
    pages[nav](data)


if __name__ == "__main__":
    main()
