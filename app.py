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

st.set_page_config(page_title="Hometree", page_icon="🌿", layout="wide")


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
            "bio": "喜欢阅读、音乐和温柔的日常，想把书和声音留在生活里。",
            "location": "上海",
            "social": {
                "douban": "豆瓣在读 126 本 · 书影音记忆中有很多微光",
                "netease": "网易云 89 首私藏 · 偏温柔与失真感",
            },
            "highlights": [
                "在读清单",
                "音频收藏",
                "城市书友",
            ],
        },
        "users": [
            {
                "id": "louye",
                "name": "娄烨",
                "age": 28,
                "img": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&w=900&q=80",
                "tags": ["电影", "城市", "文艺"],
                "quote": "我喜欢在雨天读书和听旧歌，像是把自己留在过去。",
                "ai": "适合在雨天聊电影、成长和失去。",
                "douban": "豆瓣 132 关注 · 96 篇影评",
                "netease": "网易云歌单：雨夜漫谈",
            },
            {
                "id": "bjork",
                "name": "Bjork",
                "age": 34,
                "img": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=900&q=80",
                "tags": ["Art Pop", "实验", "声音"],
                "quote": "I am the spark, and the sound is my map.",
                "ai": "喜欢极端和美丽并存的音乐、生活与书。",
                "douban": "豆瓣 89 关注 · 42 条收藏",
                "netease": "网易云：极地珊瑚",
            },
            {
                "id": "tyler",
                "name": "Tyler Durden",
                "age": 30,
                "img": "https://images.unsplash.com/photo-1520637836862-4d197d17c90a?auto=format&fit=crop&w=900&q=80",
                "tags": ["Fight Club", "沉思", "反常识"],
                "quote": "You are not your job.",
                "ai": "适合聊哲学、荒诞和不安但有趣的东西。",
                "douban": "豆瓣 101 关注 · 29 篇书评",
                "netease": "网易云：深夜躁动",
            },
            {
                "id": "lotayu",
                "name": "罗大佑",
                "age": 27,
                "img": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=900&q=80",
                "tags": ["民谣", "城市", "文学"],
                "quote": "所有的青春，都需要一个你愿意认真听的声音。",
                "ai": "更适合聊流浪、城市、时代和回忆。",
                "douban": "豆瓣 84 关注 · 52 条笔记",
                "netease": "网易云：旧城抒情",
            },
        ],
        "books": [
            {
                "id": 1,
                "title": "撒哈拉的故事",
                "author": "三毛",
                "price": 18.9,
                "city": "北京",
                "cover": "https://img1.doubanio.com/view/subject/s/public/s27214154.jpg",
                "tags": ["旅行", "散文", "人生"],
                "similar": ["哭泣的骆驼", "梦里花落知多少", "我喜欢这个世界"],
                "summary": "一本并不远行的旅行书，用温柔又古怪的文字，写下荒凉与热烈并存的人生。",
            },
            {
                "id": 2,
                "title": "月亮与六便士",
                "author": "毛姆",
                "price": 39.0,
                "city": "上海",
                "cover": "https://img9.doubanio.com/view/subject/s/public/s29810488.jpg",
                "tags": ["文学", "艺术", "经典"],
                "similar": ["人生的枷锁", "刀锋", "百年孤独"],
                "summary": "关于自由、天才与人生选择的经典之作，常被当作一部关于“为什么要活”的小说。",
            },
            {
                "id": 3,
                "title": "我在美丽的村庄里",
                "author": "阿多尼斯",
                "price": 52.0,
                "city": "广州",
                "cover": "https://img1.doubanio.com/view/subject/s/public/s33939677.jpg",
                "tags": ["诗歌", "异乡", "城市"],
                "similar": ["荒原", "时代的寓言", "海边的卡夫卡"],
                "summary": "一部既克制又有力量的散文，关于记忆、城市和自由的微光。",
            },
            {
                "id": 4,
                "title": "你当像鸟飞往你的山",
                "author": "塔拉·韦斯特弗",
                "price": 22.5,
                "city": "杭州",
                "cover": "https://img1.doubanio.com/view/subject/s/public/s1001902.jpg",
                "tags": ["成长", "女性", "自传"],
                "similar": ["成为简·奥斯汀", "白鸟过境", "北欧微风"],
                "summary": "一部成长自传，讲述如何在极端环境中找到自己的声音和方向。",
            },
            {
                "id": 5,
                "title": "琅琊榜",
                "author": "海宴",
                "price": 34.0,
                "city": "成都",
                "cover": "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=900&q=80",
                "tags": ["历史", "政治", "悬疑"],
                "similar": ["天幕之城", "大明宫词", "长安十二时辰"],
                "summary": "一部兼具大历史感与人物力度的长篇小说，写的是权谋与正义的拉扯。",
            },
            {
                "id": 6,
                "title": "以自己为名的岛屿",
                "author": "沈从文",
                "price": 36.0,
                "city": "深圳",
                "cover": "https://img9.doubanio.com/view/subject/s/public/s28065015.jpg",
                "tags": ["散文", "乡土", "文史"],
                "similar": ["湘行散记", "边城", "浮生六记"],
                "summary": "带着淡淡乡土气息与沉静笔触，写一座岛和一个人对世界的理解。",
            },
        ],
        "articles": [
            {
                "id": 101,
                "title": "在城市里，听见自己在路上",
                "category": "书评",
                "cover": "https://images.unsplash.com/photo-1516280440502-863a346513c1?auto=format&fit=crop&w=1200&q=80",
                "summary": "城市总是让人以为自己活得很快，但真正的热闹常常来自一点点安静。",
                "content": "城市的喧闹会让人急切地想加速，而真正值得珍藏的，反而是那些被打断又重新捡回来的片刻。书，是这类回声里最好的提问。它让人慢一点，认真一点，甚至允许自己在一段故事里停留足够久。你会发现，真正缓慢的并不是时间，而是你对世界的感受。",
            },
            {
                "id": 102,
                "title": "7 个晚上可以把音乐的世界打开",
                "category": "音乐",
                "cover": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=1200&q=80",
                "summary": "从民谣到实验，值得慢慢听的声音，不一定要“懂”才有意义。",
                "content": "有些音乐，不需要一上来就被理解。它先发出一声像风一样的回响，再在一个晚归的夜晚突然落到你耳朵里。我们习惯把喜欢归类成“偏好”，可音乐真正的价值，是让人重新认识自己身上的某种长久感受——孤独、温柔、骚动、放大，甚至是无声的庆祝。",
            },
            {
                "id": 103,
                "title": "读完一本书后，最重要的不是总结，而是继续认真看见生活",
                "category": "随笔",
                "cover": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?auto=format&fit=crop&w=1200&q=80",
                "summary": "故事结束后，真正开始的，是把书里的元素重新放回真实生活。",
                "content": "很多时候，我们嘴上说阅读，是为了更懂自己，其实阅读最重要的地方，是把人慢慢往真实世界里拉回来。一本好书不一定会改变命运，但它常常会让你更不肯用粗糙的方式生活。你开始愿意认真对待细节，愿意陪时间走一段，终于明白：生活不是被理解，而是被接受。",
            },
        ],
        "podcasts": [
            {
                "id": 201,
                "title": "在书和声音之间",
                "host": "Yiming",
                "cover": "https://images.unsplash.com/photo-1511379938547-c1f69419868d?auto=format&fit=crop&w=1200&q=80",
                "summary": "12 分钟里，聊聊阅读、独处和如何把一首歌留在脑海里。",
                "duration": "12:38",
                "src": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
                "type": "podcast",
            },
            {
                "id": 202,
                "title": "城市里的低声复盘",
                "host": "小雨",
                "cover": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?auto=format&fit=crop&w=1200&q=80",
                "summary": "关于一个城市、两种惯性和许多想逃离的念头。",
                "duration": "18:25",
                "src": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
                "type": "podcast",
            },
            {
                "id": 203,
                "title": "深夜独处清单",
                "host": "Yoyo",
                "cover": "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?auto=format&fit=crop&w=1200&q=80",
                "summary": "一个暗色夜晚的书单、歌单和回忆清单。",
                "duration": "15:02",
                "src": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
                "type": "podcast",
            },
        ],
        "forum_threads": [
            {
                "id": 301,
                "title": "最近最想安静分享的书是哪些？",
                "tag": "读书",
                "meta": "18 分钟前 · 12 回复",
                "desc": "我想有一段安静的读书时间，最近被《撒哈拉的故事》和《月亮与六便士》重新拯救了。你们最近有没有意外喜欢的书？",
            },
            {
                "id": 302,
                "title": "深夜听歌进行时：你最喜欢哪种氛围感？",
                "tag": "音乐",
                "meta": "26 分钟前 · 21 回复",
                "desc": "雨夜、城市灯光、咖啡和失真音响，哪种组合最容易让你停下生活？",
            },
            {
                "id": 303,
                "title": "如果把人生按一本书来命名，你会选什么？",
                "tag": "生活",
                "meta": "11 分钟前 · 9 回复",
                "desc": "我想起很多神奇的句子，但最终还是愿意用“仍然有光的地方”来给自己命名。",
            },
        ],
        "forum_replies": {
            301: [
                {"user": "栗子", "text": "我最近在重读《断裂》与《人与地》的片段，真的特别适合安静时分。"},
                {"user": "阿林", "text": "《撒哈拉的故事》会让我怀念很多难得的自由感，尤其是旅行和独处。"},
            ],
            302: [
                {"user": "Mina", "text": "我最喜欢雨夜站在地铁口听低音，像心里不想说出口的小鼓动。"},
                {"user": "小R", "text": "咖啡 + 失真 + 旧城市灯光，这个组合我一直不肯放弃。"},
            ],
            303: [
                {"user": "豆花", "text": "我会给自己命名成《慢一点，甚至还会长出一层光》。"},
                {"user": "青树", "text": "《当世界的声音安静下来》也很适合我。"},
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
        st.caption("MySQL 已连接，已加载数据库数据。")
    except Exception:
        st.caption("MySQL 连接失败，当前使用本地演示数据。")
    return data


def render_chat_panel(user: Dict[str, Any]) -> None:
    with st.sidebar:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader(f"与 {user['name']} 聊天")
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

        prompt = st.chat_input("发消息")
        if prompt:
            history = st.session_state.chat_history.setdefault(user["id"], [])
            history.append({"role": "user", "text": prompt})
            history.append({"role": "assistant", "text": "我也在想，喜欢的东西总会在某个时刻被互相理解。"})
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


def render_match_tab(data: Dict[str, Any]) -> None:
    st.title("匹配")
    st.caption("喜欢你喜欢的东西，不必大动干戈。")

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
        st.caption("匹配度 72%")

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
                [{"role": "assistant", "text": "你好，我也很喜欢你标注的这种气质。"}],
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
            st.info("还没有认识的人，试试看喜欢一位吧。")
        for u in st.session_state.matched_users:
            row = st.columns([1, 4])
            with row[0]:
                st.image(u["img"], width=52)
            with row[1]:
                if st.button(u["name"], key=f"match_{u['id']}", use_container_width=True):
                    st.session_state.selected_match = u
                    st.rerun()
                past = st.session_state.chat_history.get(u["id"], [])
                text = past[-1]["text"] if past else "已经匹配成功"
                st.caption(text[:30])
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.selected_match is not None:
        render_chat_panel(st.session_state.selected_match)


def render_market_tab(data: Dict[str, Any]) -> None:
    st.title("书市")
    st.caption("把喜欢的书，继续留在生活中。")

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
            if st.button("查看详情", key=f"detail_{book['id']}", use_container_width=True):
                st.session_state.selected_book = book
            if st.button("加入清单", key=f"bag_{book['id']}", use_container_width=True):
                st.toast(f"已加入《{book['title']}》")
            st.markdown('</div>', unsafe_allow_html=True)

    if "selected_book" in st.session_state:
        book = st.session_state.selected_book
        st.divider()
        st.subheader(f"{book['title']} 详情")
        col1, col2 = st.columns([1, 2])
        col1.image(book["cover"], use_container_width=True)
        with col2:
            st.markdown(f"**作者** {book['author']}")
            st.markdown(f"**标签** {' / '.join(book['tags'])}")
            st.markdown(f"**价格** ¥{book['price']:.2f}")
            st.markdown(f"**简介** {book['summary']}")
            st.markdown(f"**相似推荐** {' / '.join(book['similar'])}")


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
            if st.button("查看全文", key=f"article_{post['id']}", use_container_width=True):
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
            if st.button("收听", key=f"pod_{pod['id']}", use_container_width=True):
                st.session_state.selected_podcast = pod
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        if "selected_podcast" in st.session_state:
            pod = st.session_state.selected_podcast
            st.divider()
            st.subheader(pod["title"])
            st.caption(f"主播：{pod['host']} · 时长：{pod['duration']}")
            st.audio(pod.get("src", ""), format="audio/mp3")


def render_forum_tab(data: Dict[str, Any]) -> None:
    st.title("论坛")
    st.caption("分享你最近打动你的声音、书和生活感受。")

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
        st.subheader(f"讨论：{thread['title']}")
        st.write(thread["desc"])
        if thread_id in data["forum_replies"]:
            for reply in data["forum_replies"].get(thread_id, []):
                with st.chat_message("assistant"):
                    st.write(f"{reply['user']}：{reply['text']}")
        prompt = st.chat_input("写回复")
        if prompt:
            data["forum_replies"].setdefault(thread_id, []).append({"user": "你", "text": prompt})
            st.rerun()


def render_profile_tab(data: Dict[str, Any]) -> None:
    profile = data["profile"]
    st.title("我的")

    st.markdown('<div class="hero-panel">', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 3])
    with c1:
        st.image(profile["avatar"], width=180)
    with c2:
        st.markdown(f'<div class="hero-title">{profile["name"]}</div>', unsafe_allow_html=True)
        st.caption(f"{profile['location']} · 豆瓣 / 网易云")
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
    row[0].button("主页定制", use_container_width=True)
    row[1].button("兴趣标签", use_container_width=True)

    st.subheader("偏好")
    st.toggle("不被推荐", value=True)
    st.toggle("论坛提醒", value=True)
    st.toggle("书单同步", value=True)

    st.subheader("标签")
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
        p1.button("播放", key="play_demo", use_container_width=True)
        p2.button("暂停", key="pause_demo", use_container_width=True)
        p3.button("下一首", key="next_demo", use_container_width=True)


pages = {
    "匹配": render_match_tab,
    "书市": render_market_tab,
    "动态": render_dynamic_tab,
    "论坛": render_forum_tab,
    "我的": render_profile_tab,
}


def main() -> None:
    data = get_data()
    nav = st.sidebar.radio("导航", list(pages.keys()), index=0)
    pages[nav](data)


if __name__ == "__main__":
    main()
