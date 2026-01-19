# 🚀 CareerForge AI: The Agentic Career Coach

### *Bridging the Skill Gap with IBM Watsonx & Granite*

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![AI](https://img.shields.io/badge/AI-IBM%20Watsonx-blueviolet)
![SDG](https://img.shields.io/badge/SDG-8%20Decent%20Work-green)

## 📌 Project Overview
**CareerForge AI** is an intelligent, Agentic AI platform designed to help students bridge the gap between academic knowledge and industry requirements. Unlike standard resume parsers, CareerForge uses a **Multi-Agent System** to actively diagnose skill gaps and conduct personalized technical interviews to fix them.

Aligned with **UN SDG 8 (Decent Work and Economic Growth)**, this tool aims to reduce youth unemployment by providing enterprise-grade career coaching to everyone, for free.

---

## 🤖 The "Agentic" Workflow
CareerForge is powered by **IBM Granite-3-8b-instruct**, orchestrating three distinct agents:

1.  **🕵️ The Analyst Agent (Gap Analysis)**
    * Reads the user's PDF Resume.
    * Compares skills against a live `skills.json` taxonomy.
    * Identifies missing "Critical Skills" (e.g., detecting a lack of SQL or Cloud experience).

2.  **✍️ The Architect Agent (Resume Optimization)**
    * Rewrites the user's "Professional Summary" using action verbs.
    * Strategically highlights transferrable skills to hide gaps.
    * **Output:** Generates a downloadable Optimized Summary file.

3.  **🎙️ The Coach Agent (Adaptive Interviewer)**
    * **The "Handoff":** Reads the gaps found by the Analyst Agent.
    * **Dynamic Questioning:** Instead of generic questions, it specifically asks about the *missing* skills (e.g., "I see you lack ETL experience. How would you build a pipeline?").
    * **Real-time Grading:** Scores answers (0-10) and provides "Golden Answers" for learning.

---

## 🛠️ Tech Stack
* **Core AI:** IBM Watsonx.ai (Granite-3-8b-instruct)
* **Frontend:** Streamlit (Python)
* **Orchestration:** LangChain Pattern (Session State Management)
* **Data Processing:** PyPDF (PDF Parsing)

---

## 💡 Impact (SDG 8)
* **Target 8.6:** Reducing the proportion of youth not in employment, education, or training.
* **Solution:** By providing instant, AI-driven feedback, CareerForge democratizes access to high-quality interview coaching, making candidates "Job Ready" in minutes.

---

**Built for the IBM SkillsBuild Applied AI Internship 2025.**
