
# 🌳 Hometree: Privacy-First Matchmaking App

Hometree is a slow-dating platform that connects users based on shared tastes in books, movies, and music, moving away from superficial swiping.

## 👤 My Role
**Product Lead & Full-Stack Developer** (University Innovation Competition)

## 🚀 Key Product Decisions
- **Niche Positioning:** Identified the gap for "slow dating" among subculture enthusiasts (indie music, art films, literature) who are tired of traditional dating apps.
- **AI Integration:** Designed AI-powered ice-breaking mechanics using LLMs to suggest conversation starters based on shared interests.
- **Privacy-First Architecture:** Users are matched based on high-dimensional vector similarity, not photos, ensuring a safe and deep connection.

## 🛠️ Tech Stack & Architecture
- **Backend:** Python, Flask
- **Database:** MySQL (Relational database for user profiles, interest tags, and match records)
- **Algorithm:** Collaborative Filtering, User Interest Vector Cosine Similarity

## ⚙️ Core Matching Logic (Conceptual)
1. **Feature Extraction:** User input (books, movies, music) is mapped to a high-dimensional vector space.
2. **Cosine Similarity:** We calculate the cosine similarity between two users' interest vectors.
3. **Threshold Filtering:** Users with a similarity score above a specific threshold are pushed to the recommendation pool.

*(Note: Due to data privacy and security policies, the core database credentials and complete backend source code are kept private. This repository outlines the product architecture and algorithmic logic.)*
# 🌳 HomeTree - 书影音隐私性交友平台

> 让灵魂因共鸣而连接，摆脱现实身份束缚的慢节奏兴趣社交空间。

## 💡 项目简介
HomeTree 专注于「书影音」（书籍、电影、音乐）兴趣匹配。我们反感传统社交软件的“快餐式”互动与现实标签压力，致力于通过智能算法将品味相似的灵魂紧密相连，提供一个安全、私密且充满深度交流的社区。

## ⚙️ 技术实现 (Technical Implementation)
* **后端架构**：独立设计 MySQL 数据库，并使用 Python Flask 构建后端服务。
* **核心算法**：实现协同过滤算法（Collaborative Filtering / Item2Vec + 矩阵分解）及特征向量相似度匹配，快速处理千万级用户的兴趣稀疏矩阵。
* **团队协作**：四人全周期开发，涵盖市场调研、Figma 原型设计、用户测试与敏捷迭代。

## 🚀 核心功能亮点
1. **去标签化交友**：剔除学历、身高、收入等传统世俗标签，专注于纯粹的兴趣共鸣。
2. **AI 智能匹配引擎**：基于用户导入的豆瓣/Goodreads/IMDb 等书影音数据，通过 BERT/Word2Vec 提取品味向量，结合余弦相似度精准推荐搭子。
3. **隐私与安全保障**：仅在注册时进行人脸识别验证，日常隐藏个人信息，拒绝“可能认识的人”推荐，保障陌生人社交安全。
4. **深度话题互动**：支持同步听歌、观影讨论及主题房间，拒绝被动滑屏，让用户自主掌握交友节奏。
