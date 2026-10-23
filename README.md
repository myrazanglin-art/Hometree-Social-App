# 🌳 Hometree: Privacy-First Matchmaking App / 书影音隐私交友平台

> Connecting souls through resonance, breaking free from real-world identity constraints in a slow-paced interest-driven social space.
> 让灵魂因共鸣而连接，摆脱现实身份束缚的慢节奏兴趣社交空间。

## 💡 Executive Summary / 执行摘要

Hometree is a slow-dating platform that connects users based on shared tastes in books, movies, and music. By combining AI-driven taste analysis with a strict privacy-first architecture, we shift the paradigm from "looks-first" to "taste-first".
HomeTree 是一款专注于「书影音」深度兴趣匹配的慢节奏交友平台。通过结合 AI 驱动的内容分析与严格的隐私优先架构，我们将交友逻辑从“颜值导向”彻底扭转为“灵魂共鸣”。
*(Status: Winner of the 11th HKU Innovation & Entrepreneurship Competition, currently live as a Web MVP).*

## 🚨 Market Context & User Persona / 市场背景与用户画像

**The Problem:** Mainstream apps (Tinder, Bumble) optimize for superficial swiping and fast dopamine hits, causing severe "dating fatigue." Platforms like Soul become overly gamified, while Douban has deep data but lacks efficient social matchmaking.

**Target Persona:** 
- **Demographics:** 20-28 years old, Tier 1/2 cities, highly educated.
- **Psychographics:** Subculture enthusiasts (indie music fans, art film lovers, literature readers). They are introverted, socially exhausted by small talk, and crave deep, meaningful conversations.
- **Core Pain Points:** 
  1. High social pressure to present an idealized physical image.
  2. The "Cold Start" problem: Even after a match, users struggle with "Hi, hello" and the conversation dies.

主流应用（如 Tinder、探探）过度优化“看脸”滑动，导致用户产生严重的社交疲劳；而 Soul 等平台过度游戏化，豆瓣有深度数据却缺乏高效社交机制。
**目标用户**：一二线城市 20-28 岁的高知人群，小众文化爱好者。他们性格偏内向，厌恶无意义的寒暄，渴望深度的精神交流。核心痛点是：社交形象压力大，以及匹配后“不知如何开口”的冷启动尴尬。

## 🥊 Competitive Analysis & Moat / 竞品分析与护城河

| Dimension / 维度 | Tinder / 探探 | Soul | Douban / 豆瓣 | **Hometree** |
| :--- | :--- | :--- | :--- | :--- |
| **Match Logic / 匹配逻辑** | Photo & Distance | Anonymous quizzes | Content consumption | **Taste Vectors & AI** |
| **User Journey / 用户路径** | Swipe -> Chat | Avatar -> Match | Post -> Discuss | **Sync Media -> AI Ice-break** |
| **Social Pressure / 压力** | High (Visual) | Medium | Low (No match) | **Low (No photos required)** |
| **Retention Hook / 留存** | Gamification | Virtual gifts | Content quality | **Deep Emotional Connection** |

**Our Moat / 我们的壁垒:** Instead of competing on user volume, we leverage high-density taste data (via Douban/NetEase APIs) and LLMs to create a matching experience that no generic social app can replicate. 
我们不拼用户数量，而是利用高密度的品味数据，结合大语言模型，打造通用社交软件无法复制的深度匹配体验。

## 🚀 Core Product Decisions (PRD) / 核心产品决策

### 1. Privacy-First & De-tagging Architecture / 隐私优先与去标签化
- **No Photos First:** The algorithm strictly ignores physical appearance. Users interact based on text and media profiles first.
- **De-tagging:** Removes socio-economic tags (school, income, height) to eliminate materialistic bias and social hierarchy.

- **无照片优先**：算法严格屏蔽外貌干扰，用户优先基于文字与书影音档案进行互动。
- **去标签化**：剔除学历、收入、身高等世俗标签，消除物质偏见与社交阶级感。

### 2. AI Agent as a "Social Lubricant" / AI 作为“社交润滑剂”
- Upon a successful match, the LLM (integrated via OpenAI API) analyzes the overlapping dataset (e.g., both users love *Mulholland Drive*). 
- It auto-generates 3 specific, context-aware ice-breaker questions. This solves the "Cold Start" issue and increases the **Day-1 chat conversion rate**.

- 匹配成功后，系统调用大模型分析两人的重合数据（例如双方都喜欢《穆赫兰道》）。
- 系统自动生成 3 个具体的、有深度的话题卡片。这不仅解决了冷启动尴尬，更极大提升了首日聊天转化率。

## ⚙️ System Architecture & Database / 系统架构与数据库设计

I independently designed the relational database and built the backend using **Python Flask** and **MySQL**.
我独立设计了关系型数据库，并使用 Python Flask 与 MySQL 构建了完整的后端服务。

**Database Schema Highlights (MySQL):**
- **`User` Table:** Stores ID, encrypted password, privacy settings, and status.
- **`Tag` Table:** A master list of books, movies, and music with indexed IDs for fast retrieval.
- **`User_Tag` (Many-to-Many):** Records which user likes which media, including weighting (e.g., if a song is on repeat, the weight is higher).
- **`Match` Table:** Stores historical match records and the cosine similarity scores.

**Core Matching Algorithm (Collaborative Filtering & Cosine Similarity):**
1. **Feature Extraction:** Convert user media (books, movies, music) into high-dimensional vector space using BERT/Word2Vec.
2. **Cosine Similarity:** Calculate the angle between two users' interest vectors to determine taste alignment.
3. **Threshold Filtering:** Users with a similarity score > 0.75 are pushed to the recommendation pool, then refined by activity levels.

**核心匹配算法（协同过滤与余弦相似度）：**
1. **特征提取**：使用 BERT/Word2Vec 将用户的书影音数据转化为高维向量空间。
2. **余弦相似度**：计算两个用户兴趣向量的夹角，得出品味契合度。
3. **阈值过滤**：相似度得分高于 0.75 的用户进入推荐池，再根据活跃度进行精排。

## 📈 User Journey / 真实用户旅程
1. **Onboarding:** Sign up & authorize Douban/NetEase data.
2. **Matching:** AI analyzes the vector data to find the top 3 matches daily.
3. **Ice-breaking:** The AI Agent provides 3 tailored conversation starters.
4. **Deep Chat:** Chat UI features a "Vibe Check" (collaborative playlist or movie room).

1. **冷启动**：注册并授权导入豆瓣/网易云数据。
2. **匹配**：AI 分析向量数据，每日仅推荐 3 位极高契合度的候选人。
3. **破冰**：AI Agent 提供 3 个专属破冰话题。
4. **深度互动**：聊天界面支持“氛围检测”（如两人共同创建歌单、同步看电影）。

## 🛠️ Tech Stack / 技术栈
- **Frontend/App:** Streamlit (Rapid Prototyping).
- **Backend:** Python, Flask.
- **Database:** MySQL (Designed for relational integrity and matching efficiency).
- **AI/LLM:** OpenAI API (for Ice-breaking generation).
- **Deployment:** Streamlit Community Cloud.

🔗 **[Experience the Live MVP / 在线体验](https://hometree-social-app-hgrjctg3cpkjlylf2hapxe.streamlit.app/)** 
*(Note: Due to free cloud hosting, the app may take 10-20 seconds to wake up. / 注：受限于免费云服务器，加载可能需要 10-20 秒。)*

*(Note: Due to data privacy policies, core database credentials and backend source code are kept private. This repository outlines the product architecture.)*
