import streamlit as st
import pandas as pd
import numpy as np

# 1. 页面配置与极简样式
st.set_page_config(page_title="Hometree", layout="centered")

# 模拟一个极简的 UI（类似豆瓣的留白和排版）
st.markdown("""
<style>
    .main-title { font-size: 36px; font-weight: bold; margin-bottom: 0px; }
    .sub-title { font-size: 14px; color: #666; margin-bottom: 30px; }
    .quote { font-style: italic; color: #555; font-size: 16px; margin-bottom: 20px; }
    .stButton>button { width: 100%; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# 头部
st.markdown('<div class="main-title">Hometree.</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">基于书影音的隐私社交网络</div>', unsafe_allow_html=True)

# 2. 初始化本地“数据库”（持久化在当前用户的会话中）
if 'users_db' not in st.session_state:
    st.session_state.users_db = {} # 格式: { "用户名": {"password": "xxx", "tags": [], "location": "xxx"} }
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None

# 预置一些种子用户，让匹配算法有东西可以算
if not st.session_state.users_db:
    st.session_state.users_db = {
        "yuki_indie": {"password": "123", "tags": ["独立音乐", "实验电子", "艺术电影"], "location": "香港"},
        "john_doe": {"password": "123", "tags": ["摇滚乐", "科幻小说"], "location": "北京"},
        "alice_art": {"password": "123", "tags": ["小众文学", "艺术电影", "独立音乐"], "location": "上海"}
    }

# 3. 用户注册与登录
if st.session_state.logged_in_user is None:
    st.markdown("### 登录 / 注册")
    auth_mode = st.radio("请选择：", ["登录", "注册新账号"], horizontal=True)
    
    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")
    
    if auth_mode == "登录":
        if st.button("登录"):
            if username in st.session_state.users_db and st.session_state.users_db[username]["password"] == password:
                st.session_state.logged_in_user = username
                st.rerun()
            else:
                st.error("用户名或密码错误")
    else:
        location = st.text_input("你所在的城市（例如：香港）")
        if st.button("注册并登录"):
            if username in st.session_state.users_db:
                st.error("该用户名已被注册")
            elif len(username) > 0 and len(password) > 0:
                st.session_state.users_db[username] = {"password": password, "tags": [], "location": location}
                st.session_state.logged_in_user = username
                st.rerun()
            else:
                st.error("请填写完整信息")

# 4. 已登录状态下的核心功能
else:
    current_user = st.session_state.logged_in_user
    st.success(f"当前登录状态：**{current_user}**")
    
    if st.button("退出登录"):
        st.session_state.logged_in_user = None
        st.rerun()
        
    st.divider()
    
    # 模块一：管理我的书影音档案
    st.markdown("### 我的书影音档案")
    st.write("在下面选择你喜欢的标签，这决定了你能匹配到谁：")
    
    all_tags = ["独立音乐", "摇滚乐", "实验电子", "科幻小说", "艺术电影", "悬疑电影", "小众文学", "古典音乐", "二次元", "摄影"]
    user_tags = st.session_state.users_db[current_user]["tags"]
    
    selected_tags = st.multiselect("选择你的兴趣标签：", all_tags, default=user_tags)
    
    if st.button("保存档案"):
        st.session_state.users_db[current_user]["tags"] = selected_tags
        st.success("档案已保存！")

    st.divider()
    
    # 模块二：算法匹配
    st.markdown("### 灵魂匹配")
    st.write("系统将根据协同过滤算法（余弦相似度），为你寻找精神频率最接近的人。")
    
    if st.button("开始匹配"):
        if len(user_tags) == 0:
            st.warning("请先在上方选择并保存你的书影音档案！")
        else:
            # 构建数据集进行相似度计算
            all_users = list(st.session_state.users_db.keys())
            all_tags_set = list(set([tag for u in all_users for tag in st.session_state.users_db[u]["tags"]] + all_tags))
            
            if len(all_tags_set) == 0:
                st.info("目前没有足够的用户数据来计算。")
            else:
                # 构建独热编码矩阵
                data = []
                for u in all_users:
                    user_vector = [1 if t in st.session_state.users_db[u]["tags"] else 0 for t in all_tags_set]
                    data.append(user_vector)
                
                df = pd.DataFrame(data, index=all_users, columns=all_tags_set)
                
                # 计算余弦相似度
                from sklearn.metrics.pairwise import cosine_similarity
                sim_matrix = cosine_similarity(df)
                sim_df = pd.DataFrame(sim_matrix, index=all_users, columns=all_users)
                
                # 获取当前用户与其他人的相似度
                user_sims = sim_df[current_user].drop(current_user).sort_values(ascending=False)
                
                if len(user_sims) == 0:
                    st.info("目前只有你一个用户，请邀请朋友来注册测试。")
                else:
                    best_match = user_sims.index[0]
                    score = user_sims.iloc[0]
                    
                    if score > 0:
                        match_info = st.session_state.users_db[best_match]
                        st.success(f"匹配成功！与你的精神频率相似度：{score*100:.1f}%")
                        st.info(f"匹配用户：**{best_match}** (来自 {match_info['location']})\n\nTA 的书影音偏好：{', '.join(match_info['tags'])}")
                    else:
                        st.warning("目前没有与你品味重合的人，快去多添加一些标签吧！")

# 底部
st.divider()
st.caption("Hometree MVP. Built with Python & Streamlit.")
