# Hometree 社交书影音应用
# 改动摘要：
# - 保留原有匹配、售卖书籍、动态、论坛、个人主页、MySQL 可选数据源、聊天面板等业务逻辑
# - 修复 Streamlit Cloud / 运行环境未安装 mysql-connector-python 时的导入崩溃问题
# - 使用可选导入 + 运行时降级：未安装/未配置 MySQL 时自动回退到本地演示数据
# 运行方式：
#   1) pip install streamlit
#   2) 可选：pip install mysql-connector-python
#   3) streamlit run app.py
# 若环境未安装 mysql-connector-python，应用仍可正常启动并显示“当前使用本地演示数据”。

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
            color: #1e1b1b;
        }
        .stApp {
            background: linear-gradient(135deg, #f5efe8 0%, #f7f1f6 30%, #eef4f7 100%);
        }
        .block-container {
            max-width: 1480px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        [data-testid="stSidebar"] {
            background: rgba(255,255,255,0.62);
            backdrop-filter: blur(18px);
            border-right: 1px solid rgba(124, 58, 237, 0.08);
        }
        .stRadio > div {
            gap: 0.5rem;
        }
        .stRadio label {
            background: rgba(255,255,255,0.65);
            border: 1px solid rgba(77, 71, 66, 0.08);
            border-radius: 16px;
            padding: 0.75rem 1rem;
            margin-bottom: 0.4rem;
            font-weight: 600;
        }
        .stRadio label > div:first-child {
            display: none;
        }
        div[data-testid="stMetricValue"] {
            font-size: 1.2rem;
            font-weight: 700;
        }
        div[data-testid="stButton"] > button,
        div[data-testid="baseButton-secondary"] > button,
        button[kind="primary"] {
            border-radius: 14px;
            border: none;
            background: linear-gradient(135deg, #1f2937 0%, #4b5563 100%);
            color: white;
            padding: 0.65rem 1rem;
            font-weight: 600;
            box-shadow: 0 8px 20px rgba(31, 41, 55, 0.18);
        }
        div[data-testid="stButton"] > button:hover {
            filter: brightness(1.03);
            transform: translateY(-1px);
        }
        .card-shell {
            background: rgba(255,255,255,0.72);
            border: 1px solid rgba(72,72,72,0.08);
            border-radius: 26px;
            padding: 1rem;
            box-shadow: 0 16px 28px rgba(137, 136, 136, 0.08);
            margin-bottom: 1rem;
        }
        .profile-hero {
            background:
                linear-gradient(180deg, rgba(26, 18, 17, 0.06), rgba(26, 18, 17, 0.18)),
                url('https://images.unsplash.com/photo-1516280440502-863a346513c1?auto=format&fit=crop&w=1200&q=80') center/cover no-repeat;
            border-radius: 30px;
            padding: 1.2rem;
            min-height: 210px;
        }
        .profile-hero .title {
            font-size: 2.2rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
        }
        .soft-pill {
            display: inline-block;
            background: rgba(255,255,255,0.8);
            border: 1px solid rgba(0,0,0,0.04);
            border-radius: 999px;
            padding: 0.35rem 0.75rem;
            font-size: 0.76rem;
            font-weight: 600;
            margin-right: 0.5rem;
            margin-bottom: 0.5rem;
            color: #3d3d3d;
        }
        .book-cover {
            border-radius: 18px;
            overflow: hidden;
            box-shadow: 0 10px 24px rgba(0,0,0,0.12);
        }
        .friendly-image {
            border-radius: 20px;
            object-fit: cover;
            box-shadow: 0 12px 24px rgba(0,0,0,0.12);
        }
        .mini-avatar {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            object-fit: cover;
            border: 2px solid rgba(255,255,255,0.7);
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
            "bio": "喜欢书和音乐，偏爱安静、有温度的生活方式。把每一次阅读和聆听都当成跟城市对话。",
            "location": "杭州",
            "social": {
                "douban": "豆瓣：已绑定《书影音日记》· 126 条收藏",
                "netease": "网易云：最近在听《城市夜归》、民谣与电子",
            },
            "highlights": [
                "喜欢安静的独立出版",
                "收藏偏电影与文学的城市叙事",
                "正在读《在路上》《岛上书店》",
            ],
        },
        "users": [
            {
                "id": "louye",
                "name": "楼野",
                "age": 28,
                "img": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&w=900&q=80",
                "tags": ["文学", "独立书店", "慢生活"],
                "quote": "喜欢在雨天走遍每一家书店，听书页翻动的声音。",
                "ai": "偏爱日系文学、城市故事和安静的氛围音乐。",
                "douban": "豆瓣：已收藏 132 本书与 96 部电影",
                "netease": "网易云：最爱城市、民谣和爵士。",
            },
            {
                "id": "bjork",
                "name": "Bjork",
                "age": 34,
                "img": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=900&q=80",
                "tags": ["Art Pop", "电子", "视觉艺术"],
                "quote": "I am the spark, and the sound is my map.",
                "ai": "在艺术和音乐之间来回穿梭，喜欢具有实验性的表达。",
                "douban": "豆瓣：重度电影与纪录片收藏者",
                "netease": "网易云：电子、实验和氛围音乐收藏夹",
            },
            {
                "id": "tyler",
                "name": "Tyler Durden",
                "age": 30,
                "img": "https://images.unsplash.com/photo-1520637836862-4d197d17c90a?auto=format&fit=crop&w=900&q=80",
                "tags": ["Fight Club", "荒诞", "反主流"],
                "quote": "You are not your job.",
                "ai": "擅长破坏常规、重构日常，阅读偏哲学与反乌托邦。",
                "douban": "豆瓣：地域文化与电影史有较深关注",
                "netease": "网易云：重度摇滚与冷门独立歌单",
            },
            {
                "id": "lotayu",
                "name": "洛塔雨",
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
                "title": "房思琪的初恋乐园",
                "author": "林奕含",
                "price": 36.0,
                "city": "深圳",
                "cover": "https://img9.doubanio.com/view/subject/s/public/s28065015.jpg",
                "tags": ["文学", "成长"],
                "similar": ["围城", "我们仨", "失踪的孩子"],
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
        "blogs": [
            {
                "id": 201,
                "title": "一个城市的书店地图",
                "cover": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?auto=format&fit=crop&w=1200&q=80",
                "summary": "整理最近两个月走过的书店与咖啡馆，记录那些让我停下来阅读的地方。",
                "content": "我去过的每一家书店，都像一座小型的私人图书馆。这里的书架不只是摆放物品，而是撑起一个人的精神休息区。",
            },
            {
                "id": 202,
                "title": "和音乐一起出发：城市散步清单",
                "cover": "https://images.unsplash.com/photo-1511379938547-c1f69419868d?auto=format&fit=crop&w=1200&q=80",
                "summary": "把一段不长不短的散步，放进一个轻微失重的回响里。",
                "content": "散步不一定要有目的，也不一定要到达某处；它是一种把情绪沉下来、把空白留出来的方式。音乐在其中起到桥梁作用。",
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
                "title": "听歌像在做一场城市漫游，推荐你最近的片单",
                "tag": "音乐",
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
        st.markdown("<div class='card-shell'>", unsafe_allow_html=True)
        st.subheader(f"聊天 · {user['name']}")
        st.image(user.get("img") or fallback_avatar(user["name"]), width=70)
        st.caption(user["douban"])
        st.caption(user["netease"])

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
            history.append({"role": "assistant", "text": "我也挺喜欢这类书和音乐，我可以把你最近在看的清单发给你。"})
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


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

    left, right = st.columns([2, 1])
    with left:
        user = users[st.session_state.match_index]
        st.markdown('<div class="card-shell">', unsafe_allow_html=True)
        st.image(user["img"], use_container_width=True, clamp=True)
        st.subheader(user["name"])
        st.caption(f"{user['age']} 岁 · {' / '.join(user['tags'])}")
        st.markdown(f"> {user['quote']}")
        st.write(user["ai"])
        col_a, col_b = st.columns(2)

        if col_a.button("想认识", use_container_width=True):
            if user["id"] not in [u["id"] for u in st.session_state.matched_users]:
                st.session_state.matched_users.append(user)
            st.session_state.selected_match = user
            st.session_state.match_index += 1
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = {}
            st.session_state.chat_history.setdefault(user["id"], [
                {"role": "assistant", "text": "你好，我挺喜欢你的阅读列表和歌单风格，想聊聊下一本书。"}
            ])
            st.rerun()

        if col_b.button("下一位", use_container_width=True):
            st.session_state.match_index += 1
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card-shell">', unsafe_allow_html=True)
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
    st.caption("精选书单，带有书籍封面、简介和相似推荐。")

    for book in data["books"]:
        with st.container():
            st.markdown('<div class="card-shell">', unsafe_allow_html=True)
            cols = st.columns([1, 3])
            with cols[0]:
                st.image(book["cover"], width=160, output_format="JPEG")
            with cols[1]:
                st.subheader(book["title"])
                st.caption(f"{book['author']} · {book['city']} · {' / '.join(book['tags'])}")
                st.write(book["summary"])
                st.write("相似推荐：", " · ".join(book["similar"]))
                c1, c2, c3 = st.columns([1, 1, 1])
                c1.metric("价格", f"¥{book['price']:.2f}")
                c2.metric("状态", "可寄送")
                if c3.button("详情", key=f"detail_{book['id']}", use_container_width=True):
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
    article_tab, blog_tab = st.tabs(["文章", "博客"])

    with article_tab:
        for post in data["articles"]:
            st.markdown('<div class="card-shell">', unsafe_allow_html=True)
            st.image(post["cover"], use_container_width=True)
            st.subheader(post["title"])
            st.caption(f"{post['category']} · 2 分钟阅读")
            st.write(post["summary"])
            if st.button("查看详情", key=f"article_{post['id']}", use_container_width=True):
                st.session_state.selected_article = post
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        if "selected_article" in st.session_state:
            st.divider()
            post = st.session_state.selected_article
            st.subheader(post["title"])
            st.caption(post["category"])
            st.write(post["content"])

    with blog_tab:
        for blog in data["blogs"]:
            st.markdown('<div class="card-shell">', unsafe_allow_html=True)
            st.image(blog["cover"], use_container_width=True)
            st.subheader(blog["title"])
            st.write(blog["summary"])
            if st.button("打开博客", key=f"blog_{blog['id']}", use_container_width=True):
                st.session_state.selected_blog = blog
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        if "selected_blog" in st.session_state:
            st.divider()
            blog = st.session_state.selected_blog
            st.subheader(blog["title"])
            if "content" in blog:
                st.write(blog["content"])
            else:
                st.write(blog["summary"])


def render_forum_tab(data: Dict[str, Any]) -> None:
    st.title("论坛")
    st.caption("可定制的小型社区，内容可点开查看回复。")

    for thread in data["forum_threads"]:
        st.markdown('<div class="card-shell">', unsafe_allow_html=True)
        st.caption(thread["tag"])
        st.subheader(thread["title"])
        st.write(thread["desc"])
        st.caption(thread["meta"])
        if st.button("查看话题", key=f"forum_{thread['id']}", use_container_width=True):
            st.session_state.selected_forum = thread["id"]
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    if "selected_forum" in st.session_state:
        thread_id = st.session_state.selected_forum
        thread = next(t for t in data["forum_threads"] if t["id"] == thread_id)
        st.divider()
        st.subheader(f"主题：{thread['title']}")
        st.write(thread["desc"])
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

    st.markdown('<div class="profile-hero">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(profile["avatar"], width=180)
    with col2:
        st.markdown('<div class="title">%s</div>' % profile["name"], unsafe_allow_html=True)
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
