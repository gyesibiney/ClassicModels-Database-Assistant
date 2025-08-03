# 🏭 ClassicModels Database Assistant

[![Hugging Face Spaces](https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-blue.svg)](https://huggingface.co/spaces/gyesibiney/classicmodels-assistant)  
*Natural language SQL interface deployed on Hugging Face Spaces*

![Gradio Interface Screenshot](https://i.imgur.com/example-screenshot.png)

## 🌐 Live Demo
Access the production deployment:  
👉 [https://huggingface.co/spaces/gyesibiney/classicmodels-assistant](https://huggingface.co/spaces/your-username/classicmodels-assistant)

## 🚀 Key Features
- **Zero-Setup Access**: Fully hosted on Hugging Face
- **Secure Execution**: Sandboxed environment with read-only DB access
- **Auto-Scaling**: Handles traffic spikes automatically
- **Persistent Storage**: Database survives container reboots

## 🛠️ Hugging Face Specific Configuration

### Secrets Management
1. Set your Gemini API key in Space settings:Settings → Repository secrets → Add secret (GEMINI_API_KEY)
   
2. Database is pre-loaded in the Space's persistent storage:
```python
DB_NAME = "classicmodels.db"  # Automatically persists between deploys

📦 Files Included
/Repository
├── app.py               # Main application
├── classicmodels.db     # SQLite database
├── requirements.txt     # Python dependencies
└── README.md            # This file

🌟 Example Queries
-- These get translated from natural language:
"Show customers from Paris with >5 orders"
"List products needing restock this month"
"Which sales rep has the most pending orders?"
   

```



















---
title: Chat DataBase V1
emoji: 🐠
colorFrom: pink
colorTo: pink
sdk: gradio
sdk_version: 5.33.0
app_file: app.py
pinned: false
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
