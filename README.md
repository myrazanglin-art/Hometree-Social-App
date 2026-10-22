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
